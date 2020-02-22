import pingparsing
import json
from celery import Celery
import requests
import easyconf
from influxdb import InfluxDBClient
import logging


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


def insert_influxdb(client, stats, name, external_id, hostname):
    d = {
        "measurement": f"account_{external_id}",
        "tags": {
            "hostname": hostname,
            "name": name,
        },
        "fields":stats
    }
    #log.debug("write to influxdb {}".format(d))
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
                success, result_stats = ping(hostname)
                log.info("result ping {}".format(result_stats))
                if success:
                    insert_influxdb(influxdb_client, result_stats,name,
                                    external_id, hostname)
                else:
                    log.info("error on ping")




def ping(destination, count=1):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination
    transmitter.count = count
    result = transmitter.ping()
    log.debug("ping result {}".format(result))
    if result.returncode == 0:
        return True, ping_parser.parse(result).as_dict()
    return False, result

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    fetch()
    # app.start()
