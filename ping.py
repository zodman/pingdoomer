import pingparsing
import json
from celery import Celery
import requests
import easyconf
from influxdb import InfluxDBClient
import logging

# logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

# Configuration
conf = easyconf.Config("ping.yaml")
BASE_URL = conf.URL(initial="http://localhost:8000/")
INFLUXDB_CONF = conf.INFLUXDB(
    initial=dict(
        host="localhost", username="root", port="8086", password="root", database="ping"
    ),
    cast=dict,
)
CELERY_ARGS = conf.CELERY(initial={"broker": "redis://localhost"}, cast=dict)
SECONDS = conf.SECONDS(initial=30, cast=int)
TOKEN = conf.TOKEN(initial="")

headers = {"Authorization": f"Token {TOKEN}"}

# clients
app = Celery("ping", **CELERY_ARGS)

logging.basicConfig(level=logging.DEBUG)


@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    log.info("setup periodic task {}".format(SECONDS))
    sender.add_periodic_task(SECONDS * 1.0, fetch.s(), name="every {}".format(SECONDS))


@app.task
def run_ping(hostname, name, external_id):
    log.info("run_ping({},{},{})".format(hostname, name, external_id))
    influxdb_client = InfluxDBClient(**INFLUXDB_CONF)
    result_stats = ping(hostname)
    return insert_influxdb(influxdb_client, result_stats, name, external_id, hostname)


@app.task
def fetch():
    log.info("executing fetch")
    base_url = f"{BASE_URL}api/accounts/"
    resp = requests.get(base_url, headers=headers)
    resp.raise_for_status()
    resp = resp.json()
    for i in resp:
        external_id = i.get("external_id")
        name = i.get("name")
        if i.get("hosts"):
            for host in i["hosts"]:
                hostname = host["hostname"]
                run_ping.delay(hostname, name, external_id)


def insert_influxdb(client, stats, name, external_id, hostname):
    d = {
        "measurement": f"account_{external_id}",
        "tags": {"hostname": hostname, "name": name,},
        "fields": {"return_code": stats["return_code"]},
    }

    return_code = stats["return_code"]
    if return_code == 0 or return_code == 1:
        d["fields"] = stats

    log.debug("write to influxdb {}".format(json.dumps(d, indent=4)))
    return client.write_points([d])


def ping(destination, count=1):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination
    transmitter.count = count
    result = transmitter.ping()
    # log.debug("ping result {}".format(result))
    return_dict = ping_parser.parse(result).as_dict()
    return_dict["return_code"] = result.returncode
    return return_dict


if __name__ == "__main__":
    fetch()
    # app.start()
