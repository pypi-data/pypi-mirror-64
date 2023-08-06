import gevent
import json
import logging
import six
import sqlite3
import ssl
import uuid
from cement.utils import fs
from json import JSONDecodeError
from locust import TaskSet
from locust.events import request_success, request_failure, EventHook
from random import choice, randint
from string import digits, ascii_letters
from time import time
from urllib.parse import urlparse
from websocket import create_connection, WebSocketConnectionClosedException

# todo add asserts to statements to validate response.
# todo dockerize all locust things and swarm it with docker compose / scale
from benchgrape.config import DB_FILE, WS
from benchgrape.core.db import TestDataMapper, RuntimeConfigMapper
from benchgrape.core.statement import login

logger = logging.getLogger(__name__)

db_file = fs.abspath(DB_FILE)
db_conn = sqlite3.connect(db_file, isolation_level='EXCLUSIVE')


def generate_call_id():
    return ''.join(choice(digits + ascii_letters) for _ in range(6))


websocket_dropped = EventHook()


def on_websocket_dropped(ex, *args, **kwargs):
    logger.exception(
        'could not receive data from websocket, '
        'reconnecting... exception was: %s', ex
    )


websocket_dropped += on_websocket_dropped


class PubSubMixin(object):
    """
    mixin to subscribe to the org right away when the set starts.
    """
    def on_start(self):
        logger.info("on_start called")
        super(PubSubMixin, self).on_start()
        self.organizations__join()


class PickleUserMixin(object):
    mapper = None
    organization = None
    _ch_mbs = None

    def __init__(self, *args, **kwargs):
        super(PickleUserMixin, self).__init__(*args, **kwargs)
        self.mapper = mapper = TestDataMapper(db_conn, logger)
        self.config = RuntimeConfigMapper(db_conn, logger)
        self.host = mapper.get_host()
        self.user = mapper.pick_user()
        self.org = mapper.get_organization()
        self.activity_factor = self.config.get_activity()

    @property
    def channel_memberships(self):
        if not self._ch_mbs:
            params = {
                "args": [
                    self.org['id'], {'membership': True, 'page_size': 1000}
                ],
                "action": 'get_rooms',
                "ns": 'rooms',
            }

            with self.client.post(
                    "/lp/rpc/", data=json.dumps(params),
                    catch_response=True,
                    headers={
                        "Authorization": f"Token {self.auth_token}",
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    verify=False,
            ) as response:
                logger.debug('get_rooms response: %i' % response.status_code)
                if response.status_code < 200 or response.status_code > 299:
                    logger.error(
                        f'cannot receive channel memberships for '
                        f'user {self.user}. status code {response.status_code}'
                    )
                    response.failure(response.status_code)
                else:
                    self._ch_mbs = json.loads(
                        response.content
                    )['response']['results'] if response.content else {}

        if not self._ch_mbs:
            raise RuntimeError(
                f'no channel list available for user {self.user}'
            )

        logger.info(
            f'received {len(self._ch_mbs)} channels for user {self.user}'
        )
        return self._ch_mbs

    def get_random_channel(self):
        return choice(self.channel_memberships)['id']

    def on_quit(self, *args, **kwargs):
        super(PickleUserMixin, self).on_quit(*args, **kwargs)
        self.mapper.relieve_user(self.user['id'])


class WampTaskSet(PickleUserMixin, TaskSet):
    """
    task set specially for wamp driven connections (v1 of course :D).
    """

    """
    pending requests, means to store sent request ids and meta info like
    request time and call type / name.
    those infos shall be deleted when the response is received
    asynchronously via _receive.
    """
    pending = None
    ws = None
    """
    user="thread" id aka random number. not a chatgrape user id
    """
    user_id = None
    """HistoryTaskSet
    store the auth token received from the login method (http "rest").
    """
    auth_token = None

    """
    falls back to ws://localhost:8000/ws
    """
    ws_location = None
    """
    ws or wss
    """
    ws_prot = None
    """
    I could tell you a joke here but it would be a waste of time.
    this was aleady a little waste of time.
    """
    org = None

    """
    we dont know the id of the first call so we dont find a start_time.
    the first call though is the create_connection handshake so we try
    to remember if we just opened the connection so we can ignore the first
    recv event.
    """
    awaiting_login_confirmation = False

    _mb = None

    def on_start(self):
        # locust wait time depending on the chattyness configured

        # does not work for some reason...
        af = self.activity_factor
        # self.wait_time = between(# )

        # self.min_wait = int(100 * 1000 / af)
        # self.max_wait = int(1000 * 10000 / af)

        self.pending = {}
        self.auth_token = self.user['token']
        self.user_id = six.text_type(uuid.uuid4())

        # cache channel memberships upon boot
        _ = self.channel_memberships

        logger.info(
            f'starting wamp thread with:\n'
            f'organization: {self.org}\n'
            f'user: {self.user}\n'
            f'token: {self.auth_token}\n'
        )

        if not self.host:
            raise AssertionError(
                '--host must be appended to determine the websocket location.'
            )

        # always use wss except if we are connecting to http.
        prot = 'wss' if urlparse(self.host).scheme != 'http' else 'ws'
        ws_location = '{}://{}/ws'.format(
            prot, self.host.replace('http://', '').replace('https://', '')
        )

        url = "{}?auth_token={}".format(ws_location, self.auth_token)
        logger.debug('connecting to %s' % url)
        try:
            # if necessary : "cert_reqs": ssl.CERT_NONE or ssl.CERT_REQUIRED}
            self.ws = ws = create_connection(
                url, origin=self.host, sslopt={"cert_reqs": ssl.CERT_NONE}
            )
        except Exception as ex:
            error = 'cannot connect to websocket at %s. error was: %s' % (url, ex)
            logger.error(error)
            raise RuntimeError(error)
        if not ws:
            raise RuntimeError('cannot create websocket connection %s' % url)
        self.awaiting_login_confirmation = True

        def _receive():
            def reconnect():
                logger.info('reconnecting...')
                self.on_start()
                logger.info('reconnected.')

            while True:
                try:
                    res = ws.recv()
                except WebSocketConnectionClosedException as ex:
                    websocket_dropped.fire(ex=ex)
                    logger.exception(
                        'could not receive data from websocket, '
                        'reconnecting... exception was: %s', ex
                    )
                    request_failure.fire(
                        request_type='WEBSOCKET_DROP',
                        name='websocket dropped',
                        response_time=0,
                        exception=ex,
                        response_length=0
                    )
                    reconnect()
                    return

                try:
                    data = json.loads(res)
                except JSONDecodeError:
                    emsg = 'unable to decode response: %s' % res
                    logger.exception(emsg)
                    request_failure.fire(
                        request_type='MALEFORMED_RESPONSE',
                        name='Maleformed Response',
                        response_time=0,
                        exception=RuntimeError(emsg),
                        response_length=0
                    )
                    reconnect()
                    return
                except Exception as uex:
                    emsg = f'Unexpected Exception while receiving: {uex}'
                    logger.exception(emsg)
                    request_failure.fire(
                        request_type='UNEXPECTED_RECEIVE_ERROR',
                        name='unexpected receive error',
                        response_time=0,
                        exception=uex,
                        response_length=0
                    )
                    reconnect()
                    return

                """
                response type cheat sheet for the hero extending this logic :).
                Message     Type    ID  Direction   Category
                WELCOME     0    Server-to-client    Auxiliary
                PREFIX      1    Client-to-server    Auxiliary
                CALL        2    Client-to-server    RPC
                CALLRESULT  3    Server-to-client    RPC
                CALLERROR   4    Server-to-client    RPC
                SUBSCRIBE   5    Client-to-server    PubSub
                UNSUBSCRIBE 6    Client-to-server    PubSub
                PUBLISH     7    Client-to-server    PubSub
                EVENT       8    Server-to-client    PubSub
                """
                # only for serious debugging
                # logger.info(f'received payload: {data}')
                call_id = data[1]
                response_type = data[0]
                end_at = int(round(time() * 1000))
                try:
                    start_at = int(self.pending[call_id]['start_at'])
                    name = self.pending[call_id]['name']
                    # clean up this dict otherwise it gets huuuge
                    del self.pending[call_id]
                except KeyError:
                    response_time = 0
                    name = ''
                    # server to client has never a start time
                    if not self.awaiting_login_confirmation and response_type in (1, 2, 5, 6, 7):
                        logger.error(
                            'call %s has no start time or name', call_id
                        )
                    else:
                        logger.info('login done')
                        self.awaiting_login_confirmation = False
                else:
                    response_time = end_at - start_at

                logger.info(
                    f'got response for {call_id} at {end_at} '
                    f'after {response_time}ms'
                )
                event_type = 'WebSocket Recv'

                if response_type == 4:
                    """
                    last entry of wamp error response is either errorDetails on
                    pos 4 or errorDesc on pos 3 so no matter last entry it is.
                    """
                    error_msg = data.pop()
                    logger.error('CALLERROR: %s (%s)', data.pop(), error_msg)
                    request_failure.fire(
                        request_type=event_type,
                        name=name,
                        response_time=response_time,
                        response_length=0,
                        exception=RuntimeError(error_msg),
                    )
                elif response_type == 8:
                    """
                    event
                    """
                    request_success.fire(
                        request_type='Event Revc',
                        name=str(data[1].replace("http://domain/", "")),
                        response_time=0,
                        response_length=len(res),
                    )
                else:
                    """
                    currently every other response type means success.
                    deciding what response type is requested might happen
                    via the `pending` variable on request time.
                    that could come in handy sometimes I guess.
                    """
                    request_success.fire(
                        request_type=event_type,
                        name=name,
                        response_time=response_time,
                        response_length=len(res),
                    )

        def _ping():
            while True:
                np = len(self.pending.keys())
                logger.info(f'{np} calls waiting for response')
                gevent.sleep(10)
                cid = generate_call_id()
                body = '[2,"{}","http://domain/ping"]'.format(cid)
                self._send_ws(cid, 'ping', body)

        gevent.spawn(_receive)
        gevent.spawn(_ping)

    def _send_ws(self, cid, name, body):
        """
        does the actual ws sending
        """
        start_at = int(round(time() * 1000))
        logger.info(f'started call {cid} at {start_at}')
        self.pending[cid] = {
            'start_at': start_at,
            'name': name
        }
        logger.info('sending request with name %s with payload %s', name, body)
        try:
            self.ws.send(body)
        except WebSocketConnectionClosedException as ex:
            websocket_dropped.fire(ex=ex)
            request_failure.fire(
                request_type='WEBSOCKET_DROP',
                name='websocket dropped',
                response_time=0,
                response_length=0,
                exception=ex,
            )
            self.on_start()
            return
        except Exception as uex:
            logger.exception('error sending request name %s with payload %s', name, body)
            request_failure.fire(
                request_type='UNEXPECTED_TRANSMIT_ERROR',
                name='unexpected transmit error',
                response_time=0,
                response_length=0,
                exception=uex,
            )
            self.on_start()
            return

        request_success.fire(
            request_type='WebSocket Sent',
            name=name,
            # this basically is always 0ish as its just the delay of the
            # sending...but one might see connection delays. also we need
            # this count as to match whether all requests got responses
            response_time=0,
            response_length=len(body),
        )

    def send_ws(self, ns, action, *args, **kwargs):
        call_id = generate_call_id()
        positional = ','.join([str(a) for a in args]) if args else ''
        keyword = str(json.dumps(kwargs)) if kwargs else None
        payload = positional
        if kwargs:
            payload += ',' + keyword

        body = '[2,"{call_id}","http://domain/{ns}/{action}",{payload}]'.format(
            call_id=call_id, ns=ns, action=action, payload=payload
        )
        # this is t place for finding slow requests if the have special params.
        # just make the name more unique.

        name = '{}.{}.{}'.format('ws', ns, action)

        if 'description' in kwargs:
            name += f" ({kwargs.pop('description')})"

        self._send_ws(call_id, name, body)

    def send_lp(self, ns, action, *args, **kwargs):
        args += (kwargs,)
        name = '{}.{}.{}'.format('lp', ns, action)

        if 'description' in kwargs:
            name += f" ({kwargs.pop('description')})"

        params = {
            "args": args,
            "action": action,
            "ns": ns,
            "debug": {'name': name}
        }

        with self.client.post(
                "/lp/rpc/", data=json.dumps(params), name=name,
                catch_response=True,
                headers={
                    "Authorization": "Token {}".format(self.auth_token),
                    "Content-Type": "application/json; charset=utf-8",
                },
                verify=False,
        ) as response:
            logger.debug('get_users response: %i' % response.status_code)
            if response.status_code < 200 or response.status_code > 299:
                response.failure(response.status_code)

    def send(self, ns, action, *args, **kwargs):
        # default should be WS, long polling is disabled for now as it does
        # not reflect the true performance (events and subscriptions on ws).
        if WS:
            self.send_ws(ns, action, *args, **kwargs)
        else:
            self.send_lp(ns, action, *args, **kwargs)

    def on_quit(self):
        # wait for the last responses to finish.
        i = 0
        max_wait_sec = 5
        while len(self.pending) and i < max_wait_sec:
            logger.info(
                'waiting to shutdown websocket, %i responses missing.',
                len(self.pending)
            )
            gevent.sleep(1)
            i += 1
        if i == max_wait_sec:
            logger.error(
                'waited for %i seconds but there are still %i requests '
                'missing. killing websocket.', i, len(self.pending)
            )
        self.ws.close()
        self.logger.info('websocket closed.')
