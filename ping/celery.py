import pingparsing
import json
from celery import Celery
import requests
import easyconf
from influxdb import InfluxDBClient
import logging
import os

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
PING_SECONDS = conf.PING_SECONDS(initial=30, cast=int)
BLACKLIST_SECONDS = conf.BLACKLIST_SECONDS(initial=30, cast=int)
TOKEN = conf.TOKEN(initial="")

headers = {"Authorization": f"Token {TOKEN}"}

# clients
app = Celery("ping", include=['ping.tasks',], **CELERY_ARGS)


@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    log.info("setup periodic task")
    from .tasks import fetch
    sender.add_periodic_task(PING_SECONDS * 1.0, fetch.s("ping", debug=False), name="every {}".format(PING_SECONDS))
    sender.add_periodic_task(BLACKLIST_SECONDS * 1.0, fetch.s("blacklist", debug=False), name="every {}".format(BLACKLIST_SECONDS))

if __name__ == "__main__": # pragma: no cover
    app.start()
