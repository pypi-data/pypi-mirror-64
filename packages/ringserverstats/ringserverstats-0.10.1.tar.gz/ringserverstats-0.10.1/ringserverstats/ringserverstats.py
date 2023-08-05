__version__ = '0.10.1'
import psycopg2
import geohash2
import logging
from geolite2 import geolite2
import click
import re
from typing import List, Dict, Union
from hashlib import sha256
from base64 import b64encode
from datetime import datetime

Event = Dict[str,Union[str, Dict]]

logger = logging.getLogger('ringserverstats')
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def parse_ringserver_log(filename: str) -> List[Event]:
    """
    Read a txlog file and parses information.
    Returns a list of events (dictionary)
    """
    logstart_pattern = r'START CLIENT (?P<hostname>\b(?:[0-9A-Za-z][0-9A-Za-z-]{0,62})(?:\.(?:[0-9A-Za-z][0-9A-Za-z-]{0,62}))*(\.?|\b)) \[(?P<ip>(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9]))\] \((?P<agent>.*)\) @ (?P<timestamp>[0-9]+-[0-9]+-[0-9]+ (?:2[0123]|[01]?[0-9]):(?:[0-5][0-9]):(?:[0-5][0-9])).*'
    logevent_pattern = '(?P<network>[A-Z0-9]*)_(?P<station>[A-Z0-9]*)_(?P<location>[A-Z0-9]*)_(?P<channel>[A-Z0-9]*)/MSEED (?P<bytes>[0-9]+) (?P<packets>[0-9]+)'
    georeader = geolite2.reader()
    process_events = True

    events = []
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        linecount = 0
        for log in file:
            linecount +=1
            logger.debug(filename + ":"+str(linecount) +" "+ log)
            # log line exemple: START CLIENT 52.red-88-2-197.staticip.rima-tde.net [88.2.197.52] (SeedLink|SeedLink Client) @ 2016-11-28 00:00:00 (connected 2016-11-26 16:37:07) TX
            if log.startswith('START CLIENT'):
                events_data = re.search(logstart_pattern, log)
                if events_data == None:
                    logger.warning("Unable to parse START log at %s:%d : %s"%(filename, linecount, log))
                    process_events = False
                    continue
                events_data = events_data.groupdict()
                location = georeader.get(events_data['ip'])
                # hash location and get the city name
                if location != None:
                    events_data['geohash'] = geohash2.encode(location['location']['latitude'], location['location']['longitude'])
                    try:
                        events_data['countrycode'] = location['country']['iso_code']
                    except KeyError:
                        events_data['countrycode'] = ''
                    try:
                        events_data['city'] = location['city']['names']['en']
                    except KeyError:
                        events_data['city'] = ''

                else:
                    logger.warning("No location available at %s:%d : %s\nAssuming it was in Grenoble"%(filename, linecount, log))
                    events_data['geohash'] = 'u0h0fpnzj9ft'
                    events_data['city'] = 'Grenoble'
                    events_data['countrycode'] = 'FR'
                # hash hostname
                events_data['hostname'] = b64encode(sha256(events_data['hostname'].encode()).digest())[:12].decode() # overcomplicated oneliner to hash the hostname
                logger.debug(events_data)
            elif log.startswith('END CLIENT'):
                process_events = True
            elif process_events:
                # line exemple :
                # FR_SURF_00_HHZ/MSEED 21511168 42014
                event = re.search(logevent_pattern, log)
                if event == None:
                    logger.warning("Unable to parse log at %s:%d : %s"%(filename, linecount, log))
                    continue
                event = event.groupdict()
                logger.debug(event)
                events.append({**events_data, **event})
    return(events)

@click.command()
@click.option('--dbhost',  'dbhost',   help='Postgres hostname or adress.', envvar='DBHOST')
@click.option('--dbport',  'dbport',   help='Postgres port. Default: 8086', envvar='DBPORT', default=5432, type=click.INT)
@click.option('--dbname',    'dbname',   help='Postgres database.', envvar='DBNAME')
@click.option('--dbuser',  'dbuser',   help='Postgres user', envvar='DBUSER')
@click.option('--dbpass',  'password', help='Postgres pass', envvar='DBPASS')
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def cli(dbhost: str, dbport: int, dbname: str, dbuser: str, password: str, files: List):
    for f in files:
        json_data = []
        logger.info("Opening file %s"%(f))
        # Parsing events from a logfile
        lastevent_time = 0
        firstevent_time = 0
        for event in  parse_ringserver_log(f):
            # get the first event time
            if firstevent_time == 0 or firstevent_time > event['timestamp']:
                firstevent_time = event['timestamp']
            # get the last event time
            if lastevent_time == 0 or lastevent_time < event['timestamp']:
                lastevent_time = event['timestamp']
            # Constructing an influxdb data from the event
            json_data.append(
                {
                    "network": event['network'],
                    "station": event['station'],
                    "location": event['location'],
                    "channel": event['channel'],
                    "city":    event['city'],
                    "country": event['countrycode'],
                    "agent":   event['agent'],
                    "client": event['hostname'],
                    "time": event['timestamp'],
                    "bytes": int(event['bytes']),
                    "geohash": event['geohash']   # high cardinality, do not index
                }
            )

        if dbhost != None :
            logger.info("Storing %d metrics"%len(json_data))
            try:
                logger.debug("host     = "+dbhost)
                logger.debug("database = "+dbname)
                logger.debug("username = "+dbuser)
                conn = psycopg2.connect(host     = dbhost,
                                        port     = dbport,
                                        dbname   = dbname,
                                        user     = dbuser,
                                        password = password
                )
                cur = conn.cursor()
                for i in json_data:
                    cur.execute("""
                    INSERT INTO ringserver_events (time, bytes, client, network, station, location, channel, city, country, agent, geohash)
                    VALUES (%(time)s, %(bytes)s, %(client)s, %(network)s, %(station)s, %(location)s, %(channel)s, %(city)s, %(country)s, %(agent)s, %(geohash)s);
                    """, i)
                conn.commit()
                cur.close()
                conn.close()
                logger.info("Done")

            except Exception as e:
                logger.error("Error writing to postgres %s:%d database %s"%(dbhost,dbport,dbname))
                logger.error(e)

if __name__ == "main":
    cli()
