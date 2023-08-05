from ringserverstats import parse_ringserver_log, register_events, __version__
from flask import Flask, Response, request
import os
import sys

application = Flask(__name__)
application.config['DATABASE_URI'] = os.environ.get('DATABASE_URI')
if not application.config['DATABASE_URI']:
    print("DATABASE_URI environment variable required.")
    sys.exit(0)


@application.route("/", methods=['POST'])
def register_log():
    data = request.get_data().decode('utf-8')
    events = parse_ringserver_log(data)
    register_events(events, application.config['DATABASE_URI'])

@application.route("/", methods=['GET'])
def about():
    return Response("Ringserverstats version %s parses ringserver daily txlog messages.\nSend the logfile in a POST request to register in the Database"%(__version__))

if __name__ == "__main__":
    application.run(host='0.0.0.0')
