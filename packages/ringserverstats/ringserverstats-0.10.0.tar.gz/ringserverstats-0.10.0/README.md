# ringserverstats

Parse ringserver reports, compute statistics and store in influxdb.

![ringserver activity](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-30.png)

![ringserver statistics by day](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-30_1.png)

![ringserver statistics by month](https://github.com/resif/ringserver-stats/raw/master/images/2019-02-25_09-31.png)

## Installation

ringserverstats is distributed on PyPI https://pypi.org as a universal wheel.

``` bash
    $ pip install ringserverstats
```

## Postgresql preparation

``` sql
CREATE ROLE resifstats WITH LOGIN PASSWORD 'md5xxxxxxxxxx';
CRATE DATABASE resifstats OWNER resifstats;
\c resifstats
CREATE EXTENSION timescaledb
```

Then go for the migrations :

``` bash
$ yoyo apply --database postgresql://resifstats@resif-pgdev.u-ga.fr:5433/resifstats -m migrations
```

## Usage

To work properly, this program needs the following environment variables set :

  * `DBHOST` : The host name or adress of influxdb server
  * `DBPORT` : The port number of influxdb server
  * `DBUSER` : The influxdb user to authenticate to
  * `DBPASS` : The password to authenticate with
  * `DBNAME`   : The database name containing the metric

``` bash
$ ringserverstats txlogs.log
```

## Explanations

The TX logs from ringserver are metrics suitable for a timeserie database. The idea is to parse the logs, as in the exemple below, and to generate values to insert into an influxdb timeseries database.

The file `grafana-dashboard.json` can be imported into grafana to visualize this timeserie.

### Events

The ringserverevents measure has several tags :

  * network, station, location, channel : which data was requested
  * geohash : location of the client in geohash format
  * hosthash : a hash of the client ip (usefull to correlate the clients requests)
  * city : an english city name

### Grouping and downsampling
To achieve downsampling, we use timescaledb's continuous query. 

## License

`ringserverstats` is distributed under the terms of the GPL v3 or later. See LICENSE file.

## Build

``` shell
python3 setup.py sdist bdist_wheel
```

## Test

``` shell
tox
```
