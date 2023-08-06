import json
import os
import subprocess
import time
from cement import Controller, ex, fs
from locust.clients import HttpSession
from multiprocessing import cpu_count

from benchgrape.core.db import TestDataMapper, RuntimeConfigMapper
from benchgrape.core.statement import login
from benchgrape.core.utils import DEFAULT_TOKEN_LOCATION

activity_map = {
    "lazy": 1,
    "chatty": 5,
    "crazy": 25,
    "mechanical_keyboard": 100,
}


"""
args we always need for a benchmark
"""
base_args = [
    (['--url'], {
        'help': 'url, example: http://chatgrape.com/',
        'action': 'store',
        'required': True
    }),
    (['--port'], {
        'help': 'port to connect to, defaults to 443',
        'action': 'store',
        'default': 443
    }),
    (['--org'], {
        'help': 'organization id, defaults to 1',
        'action': 'store',
        'default': 1
    }),
    (['--websockets'], {
        'help': 'number of websockets to connect, defaults to 100',
        'action': 'store',
        'default': 100
    }),
    (['--logpath'], {
        'help': 'Path to for files, defaults to ./logs',
        'action': 'store',
        'default': './logs'
    }),
    (['--duration'], {
        'help': 'duration of the benchmark in seconds, defaults to 60',
        'action': 'store',
        'default': 60
    }),
    (['--hatchrate'], {
        'help': 'how many clients spawn per second, default to websockets/60',
        'action': 'store',
        'default': 60
    }),
    (['--activity'], {
        'help': 'how active the users are, choices are: '
                '"lazy", "chatty", "crazy", "mechanical_keyboard"',
        'action': 'store',
        'default': 'lazy'
    }),
]

singleuser_benchmark_args = base_args.copy()
singleuser_benchmark_args.extend([
    (['--username'], {
        'help': 'email/username used for login (only for non-token mode)',
        'action': 'store',
        'default': None
    }),
    (['--password'], {
        'help': 'password used for login. hint: 2fa is not '
                'supported, use an auth token instead if the account has 2fa '
                'enabled.',
        'action': 'store',
        'default': None
    }),
    (['--token'], {
        'help': 'if auth token is provided, username and password is not '
                'needed.',
        'action': 'store',
        'default': None
    }),
])

multiuser_benchmark_args = base_args.copy()
multiuser_benchmark_args.extend([
    (['--tokens'], {
        'help': 'Path to user file. ',
        'action': 'store',
        'default': DEFAULT_TOKEN_LOCATION
    }),
    (['--slaves'], {
        'help': 'number of slaves to spawn, number of cpu -1 is default',
        'action': 'store',
        'default': cpu_count() - 1
    }),
])


class Benchmark(Controller):
    class Meta:
        label = 'benchmark'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(
        help='singleuser mode',
        arguments=singleuser_benchmark_args
    )
    def single_user(self):
        n_ws = self.app.pargs.websockets
        url = self.app.pargs.url
        port = self.app.pargs.port
        url = f"{url}:{port}"

        username = self.app.pargs.username
        password = self.app.pargs.password
        token = self.app.pargs.token
        duration = self.app.pargs.duration
        org_id = self.app.pargs.org

        activity_factor = activity_map[self.app.pargs.activity]

        hatchrate = self.app.pargs.hatchrate or int(n_ws/60)
        # DEBUG/INFO/WARNING/ERROR/CRITICAL
        loglevel = 'INFO'

        logpath = fs.abspath(self.app.pargs.logpath)

        self.app.log.debug('creating log directory and log files.')
        fs.ensure_parent_dir_exists(logpath)
        fs.ensure_dir_exists(logpath)
        debug_fname = fs.join(logpath, 'debug.log')
        stats_fname = fs.join(logpath, 'stats.log')
        open(debug_fname, 'a').close()
        open(stats_fname, 'a').close()

        self.app.log.info('establish %s websocket connections to server %s '
                          'with user %s. press crtl+c to stop the test.' %
                          (n_ws, url, username))

        self.app.log.info(
            'establish %s websocket connections to server %s. '
            'press crtl+c to stop the test.' % (n_ws, url)
        )

        runtime_config = RuntimeConfigMapper(self.app.db, self.app.log)
        # make sure we always get the same user from the user backend by
        # enabling recycling and only have one user.
        runtime_config.enable_user_recycliing()
        runtime_config.set_activity(activity_factor)

        mapper = TestDataMapper(self.app.db, self.app.log)
        self.app.log.info(
            'logging in...'
        )
        if not token:
            token = login(HttpSession(base_url=url), username, password)
            self.app.log.info(f"got token {token}")

        if not token:
            raise RuntimeError(
                f"login at {url} failed. stopping, wont connect to websocket."
            )
        self.app.log.info(
            'login successful. dropping all existing benchmark users to have '
            'a unique user to test with.'
        )
        mapper.drop_db()
        mapper.init_db()
        # int(u['id']), u['username'], u['password'], u['token']
        mapper.sync_db(
            {
                'id': org_id, 'url': url, 'name': '', 'subdomain': ''
            }, [{
                'id': 0, 'username': username, 'password': password,
                'token': token
            }]
        )
        self.app.log.info(
            'successfully added the test user, starting locust. '
            'visit the URL in the browser which will be displayed below '
            'in a few seconds.'
        )

        locust_file = fs.abspath(fs.join(
            os.path.dirname(__file__), '../locust/locustfiles/locustfile.py'
        ))
        self.app.log.info(f'using locustfile {locust_file}')
        assert os.path.isfile(locust_file), \
            f"locust file {locust_file} does not exist."


        l_args = [
            f"--locustfile={locust_file}",
            # f"--logfile={fs.abspath(stats_fname)}", stdout for now
            f"--loglevel={loglevel}",
            #f"--host={url}",
            #f"--port={port}",
            #f"--hatch-rate={hatchrate}",
            #f"--clients={n_ws}",
            #f"--run-time={duration}"

        ]

        self.app.log.info(f'running locust {" ".join(l_args)}')
        subprocess.run([
            "locust",
            *l_args
        ])

    @ex(
        help='multiuser mode (needs user json file). This will also start a '
             'master-slave benchmark which will use all your CPUs so '
             'buckle up and save your open word documents.',
        arguments=multiuser_benchmark_args
    )
    def multi_user(self):
        n_ws = self.app.pargs.websockets
        n_slaves = int(self.app.pargs.slaves)
        url = self.app.pargs.url
        port = self.app.pargs.port
        url = f"{url}:{port}"

        org_id = self.app.pargs.org

        activity_factor = activity_map[self.app.pargs.activity]

        # DEBUG/INFO/WARNING/ERROR/CRITICAL
        loglevel = 'INFO'

        logpath = fs.abspath(self.app.pargs.logpath)

        self.app.log.debug('creating log directory and log files.')
        fs.ensure_parent_dir_exists(logpath)
        fs.ensure_dir_exists(logpath)
        debug_fname = fs.join(logpath, 'debug.log')
        stats_fname = fs.join(logpath, 'stats.log')
        open(debug_fname, 'a').close()
        open(stats_fname, 'a').close()

        runtime_config = RuntimeConfigMapper(self.app.db, self.app.log)
        mapper = TestDataMapper(self.app.db, self.app.log)

        # make sure we always get the same user from the user backend by
        # enabling recycling and only have one user.
        #runtime_config.enable_user_recycliing()
        runtime_config.disable_user_recycling()

        # todo not working but also not super important
        runtime_config.set_activity(activity_factor)

        users = []
        i = 0
        # todo swapt that to somehwere else
        with open(self.app.pargs.tokens) as json_file:
            data = json.load(json_file)
            for token in data['tokens']:
                users.append({
                    'id': i, 'username': f'user-{i}', 'password': None,
                    'token': token
                })
                i += 1

        mapper.drop_db()
        mapper.init_db()
        mapper.sync_db(
            {'id': org_id, 'url': url, 'name': '', 'subdomain': ''}, users
        )
        self.app.log.info(
            'successfully added the test user, starting locust. '
            'visit the URL in the browser which will be displayed below '
            'in a few seconds.'
        )
        # set all users to not-active
        mapper.sanitize()
        available = mapper.available_user_count()
        self.app.log.info((f"{available} users are ready to spam."))

        locust_file = fs.abspath(fs.join(
            os.path.dirname(__file__), '../locust/locustfiles/locustfile.py'
        ))
        self.app.log.info(f'using locustfile {locust_file}')
        assert os.path.isfile(locust_file), \
            f"locust file {locust_file} does not exist."

        l_args_master = [
            f"--locustfile={locust_file}",
            f"--loglevel={loglevel}",
            f"--master",
        ]

        l_args_slave = [
            f"--locustfile={locust_file}",
            f"--loglevel={loglevel}",
            f"--slave",
            f"--master-host=127.0.0.1"
        ]

        self.app.log.info(f'booting master locust {" ".join(l_args_master)}')
        procs = []
        master_proc = subprocess.Popen([
            "locust",
            *l_args_master
        ])
        procs.append(master_proc)
        self.app.log.info(
            f'booting {len(procs)-1} slaves{" ".join(l_args_slave)}'
        )
        for _ in range(0, n_slaves):
            slave_proc = subprocess.Popen([
                "locust",
                *l_args_slave
            ])
            procs.append(slave_proc)

        # check if a process finished/crashed and finish
        while True:
            time.sleep(5)
            # check if either sub-process has finished
            for proc in procs:
                proc.poll()
                if proc.returncode is not None:
                    self.app.log.info(f'{proc} is done.')
                    break

    @ex(
        help='establishes n connections to the server and make a long-running '
             'stability test of the websocket. log everything that seems '
             'unusual. can help a lot when debugging connection issues. ',
        arguments=singleuser_benchmark_args
    )
    def websocket_stability(self):
        n_ws = self.app.pargs.websockets
        url = self.app.pargs.url
        port = self.app.pargs.port
        url = f"{url}:{port}"

        username = self.app.pargs.username
        password = self.app.pargs.password
        token = self.app.pargs.token
        duration = self.app.pargs.duration
        org_id = self.app.pargs.org

        activity_factor = activity_map[self.app.pargs.activity]

        hatchrate = self.app.pargs.hatchrate or int(n_ws/60)
        # DEBUG/INFO/WARNING/ERROR/CRITICAL
        loglevel = 'INFO'

        logpath = fs.abspath(self.app.pargs.logpath)

        self.app.log.debug('creating log directory and log files.')
        fs.ensure_parent_dir_exists(logpath)
        fs.ensure_dir_exists(logpath)
        debug_fname = fs.join(logpath, 'debug.log')
        stats_fname = fs.join(logpath, 'stats.log')
        open(debug_fname, 'a').close()
        open(stats_fname, 'a').close()

        self.app.log.info('establish %s websocket connections to server %s '
                          'with user %s. press crtl+c to stop the test.' %
                          (n_ws, url, username))

        self.app.log.info(
            'establish %s websocket connections to server %s. '
            'press crtl+c to stop the test.' % (n_ws, url)
        )

        runtime_config = RuntimeConfigMapper(self.app.db, self.app.log)
        # make sure we always get the same user from the user backend by
        # enabling recycling and only have one user.
        runtime_config.enable_user_recycliing()
        runtime_config.set_activity(activity_factor)

        mapper = TestDataMapper(self.app.db, self.app.log)
        self.app.log.info(
            'logging in...'
        )
        if not token:
            token = login(HttpSession(base_url=url), username, password)
            self.app.log.info(f"got token {token}")

        if not token:
            raise RuntimeError(
                f"login at {url} failed. stopping, wont connect to websocket."
            )
        self.app.log.info(
            'login successful. dropping all existing benchmark users to have '
            'a unique user to test with.'
        )
        mapper.drop_db()
        mapper.init_db()
        # int(u['id']), u['username'], u['password'], u['token']
        mapper.sync_db(
            {
                'id': org_id, 'url': url, 'name': '', 'subdomain': ''
            }, [{
                'id': 0, 'username': username, 'password': password,
                'token': token
            }]
        )
        self.app.log.info(
            'successfully added the test user, starting locust. '
            'visit the URL in the browser which will be displayed below '
            'in a few seconds.'
        )

        locust_file = fs.abspath(fs.join(
            os.path.dirname(__file__), '../locust/locustfiles/stability.py'
        ))
        self.app.log.info(f'using locustfile {locust_file}')
        assert os.path.isfile(locust_file), \
            f"locust file {locust_file} does not exist."

        l_args = [
            f"--locustfile={locust_file}",
            # f"--logfile={fs.abspath(stats_fname)}", stdout for now
            f"--loglevel={loglevel}",
            #f"--host={url}",
            #f"--port={port}",
            #f"--hatch-rate={hatchrate}",
            #f"--clients={n_ws}",
            #f"--run-time={duration}"

        ]

        self.app.log.info(f'running locust {" ".join(l_args)}')
        subprocess.run([
            "locust",
            *l_args
        ])
