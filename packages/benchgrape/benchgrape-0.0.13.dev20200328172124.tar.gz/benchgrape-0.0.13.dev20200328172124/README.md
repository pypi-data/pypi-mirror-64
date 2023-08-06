# This is how you Bench a Grape!

locust benchmarks for chatgrape with websockets/wamp and long polling as well
as websocket stability reports.

# Installation from PyPi Package
```
pip install benchgrape
```
**virtualenv recommended**, see below

## PyPi package installation in virtualenv
```
sudo apt install python3-venv python3-pip
pip3 install virtualenv
mkdir benchgrape
cd benchgrape
virtualenv -p python3 .
source ./bin/activate
pip install benchgrape
benchgrape --help
```

## Upgrading
`pip install --upgrade benchgrape`

# Deployments (currently broken and not maintained)
## Docker
Included is a basic `Dockerfile` for building and distributing `Bench Grape`,
and can be built with the included `make` helper:

```
make docker
docker run -it benchgrape --help
```

# Usage
## Test Websocket Stability
connect a good amount of websockets to a server and monitor their stability. can be done with a single user which is passed in the args.
``` bash
benchgrape benchmark websocket-stability --url http://localhost --port 8000 --username admin --password 'quote-if-special-chars' --org 1 --websockets 10 --activity mechanical_keyboard
```

go to the web interface and have fun

## Single User Benchmark
does crazy requests and tries to massacre your grape server
```bash
benchgrape benchmark single-user --url http://localhost --port 8000 --username admin --password admin --org 1 --websockets 10 --activity mechanical_keyboard
```

## Multi User Benchmark
This feature is work in progress!
Login multiple different users
### Generating Credentials in Grape for multiple users 

```
grape@deploy:/srv/grape$ python manage.py shell_plus
# do not user all users, use "filter" for bechmark users!
import json
tokens = []

for u in User.objects.all():
    t, _=Token.objects.get_or_create(user=u)
    tokens.append(t.key)
    
data = {
    'tokens': tokens,
}
with open('/tmp/benchmark_tokens.json', 'w') as outfile:
    json.dump(data, outfile)

exit
exit

docker cp 1504c01d3679:/tmp/benchmark_tokens.json ~/workspace/benchgrape/
```

### running multiuser mode
```bash
benchgrape benchmark multi-user --url http://localhost --port 8000 --username admin --password admin --org 1 --websockets 10 --activity mechanical_keyboard --tokens ./benchmark_tokens.json
```

## Start the configured Benchmark
* visit http://localhost:8089/
* select amount of users/(which is connections for websocket stability), f.e. 100
* select hatch rate, this is the amount of users per second which will connect. weaker systems should not go over 10.
* start and watch.
* logs in ./logs/stats.log and ./logs/debug.log

## Master Slave Setups
using locust directly for master-slave setup, currently:
`locust --help`

* running one process of locust is bound to 1 CPU max and handles roughly 500 
users per CPU core. for serious stuff you need to check how much CPU your 
python request process uses, if it hits the 90s, proceed with master/slave setup. 

* start one master like this: 
`benchgrape benchmark single-user --master --url http://localhost --port 8000 --username admin --password admin --org 1 --websockets 10 --activity mechanical_keyboard`
* start at least one slave like this: 
`locust --slave --master-host=MASTER_HOST_OR_IP`


## Interpreting the Result
```
Type 	Name 	# Requests 	# Fails 	Median (ms) 	Average (ms) 	Min (ms) 	Max (ms) 	Average size (bytes) 	Current RPS
WebSocket Recv 		100 	0 	0 	0 	0 	0 	51 	0
GET 	/api/accounts/session/ 	100 	0 	290 	336 	251.3880729675293 	953.8741111755371 	356 	0
WebSocket Recv 	ping 	211 	0 	-9977 	-9984 	-10001 	0 	19 	10
WebSocket Sent 	ping 	211 	0 	0 	0 	0 	0 	33 	10
	Total 	622 	0 	0 	-3333 	-10001 	953.8741111755371 	83 	20
```
there should be no **# Fails** and no **WEBSOCKET_DROP** events in the list. only
* `WebSocket Recv`
* `GET /api/accounts/session/`
* `WebSocket Sent Ping`
* `WebSocket Recv Ping`

* the hostname is passed in the locust command and taken from there.
* heads up: if 2fa is on, the login wont work. you need to pass the token directly.

# Development

```
cd benchgrape
python3 -m pip install --upgrade pip
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python setup.py develop # -> uses the live code for development
benchgrape --help # see if the command line tool is linked and works
make test
```

Revert an installed package to continue development, switch between
```
python setup.py install
python setup.py develop
```

## Releasing to PyPi
Before releasing to PyPi, you must either configure your login credentials or
you will be prompted every time upon upload

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
make dist
make dist-upload
```
