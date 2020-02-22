import pingparsing
import json
from celery import Celery
import requests
import easyconf
from influxdb import InfluxDBClient
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

conf = easyconf.Config("ping.yaml")
BASE_URL= conf.URL(initial="http://localhost:8000/")
INFLUXDB_CONF = conf.INFLUXDB(initial=dict(host="localhost",username='root',
                                           port="8086",
                                           password='root',database="ping"),
                              cast=dict)

# clients
app = Celery("ping", broker="redis://localhost")


@app.task
def run_ping(destination):
    result = ping(destination)


def insert_failed(client, result, name, external_id, hostname):
    d = {
        "measurement": f"account_{external_id}",
        "tags": {
            "hostname": hostname,
            "name": name,
        },
        "fields":{
            "status_code": result.returncode
        }
    }

    return client.write_points([d])


def insert_influxdb(client, stats, name, external_id, hostname):
    d = {
        "measurement": f"account_{external_id}",
        "tags": {
            "hostname": hostname,
            "name": name,
        },
        "fields":{
            'return_code': stats["return_code"]
        }
    }

    return_code = stats["return_code"]
    if return_code == 0 or return_code == 1:
        d["fields"]=stats

    log.debug("write to influxdb {}".format(json.dumps(d, indent=4)))
    return client.write_points([d])


def fetch():
    base_url = f"{BASE_URL}api/accounts/"
    resp = requests.get(base_url).json()
    influxdb_client = InfluxDBClient(**INFLUXDB_CONF)
    for i in resp:
        external_id= i.get("external_id")
        name = i.get("name")
        if i.get("hosts"):
            for host in i["hosts"]:
                hostname = host["hostname"]
                result_stats = ping(hostname)
                #log.info("result ping {}".format(result_stats))
                insert_influxdb(influxdb_client, result_stats,name,
                                    external_id, hostname)




def ping(destination, count=1):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination
    transmitter.count = count
    result = transmitter.ping()
    # log.debug("ping result {}".format(result))
    return_dict = ping_parser.parse(result).as_dict()
    return_dict["return_code"]= result.returncode
    return return_dict

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    fetch()
    # app.start()
