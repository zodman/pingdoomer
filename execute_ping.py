import pingparsing

import json
import pingparsing


def ping(destination, count=1):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination
    transmitter.count = count
    result = transmitter.ping()
    return ping_parser.parse(result).as_dict()

res = ping("google.com", count=5)
print(json.dumps(res, indent=4))

