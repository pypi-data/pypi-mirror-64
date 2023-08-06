import os
import subprocess

from cement import Controller, ex, fs
from locust.clients import HttpSession

from benchgrape.core.db import TestDataMapper, RuntimeConfigMapper
from benchgrape.core.statement import login

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
    (['--users'], {
        # todo format description
        'help': 'Path to user file. ',
        'action': 'store',
        'default': './users.csv'
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
            }], [], []
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
            f"--host={url}",
            f"--logfile={fs.abspath(stats_fname)}",
            f"--port={port}",

            f"--loglevel={loglevel}",
            f"--hatch-rate={hatchrate}",
            f"--clients={n_ws}",
            f"--run-time={duration}"

        ]

        self.app.log.info(f'running locust {" ".join(l_args)}')
        subprocess.run([
            "locust",
            *l_args
        ])

        subprocess.run([
            "locust",
            "--locustfile=./benchgrape/locust/locustfiles/locustfile.py",
            "--host=%s" % "https://staging.chatgrape.com/"
        ])

    @ex(
        help='multiuser mode (needs user csv file)',
        arguments=multiuser_benchmark_args
    )
    def multi_user(self):
        subprocess.run([
            "locust",
            "--locustfile=./benchgrape/locust/locustfiles/locustfile.py",
            "--host=%s" % "https://staging.chatgrape.com/"
        ])

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
            }], [], []
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
            f"--host={url}",
            f"--logfile={fs.abspath(stats_fname)}",
            f"--port={port}",

            f"--loglevel={loglevel}",
            f"--hatch-rate={hatchrate}",
            f"--clients={n_ws}",
            f"--run-time={duration}"

        ]

        self.app.log.info(f'running locust {" ".join(l_args)}')
        subprocess.run([
            "locust",
            *l_args
        ])

        subprocess.run([
            "locust",
            "--locustfile=./benchgrape/locust/locustfiles/stability.py",
            "--host=%s" % "https://staging.chatgrape.com/"
        ])
