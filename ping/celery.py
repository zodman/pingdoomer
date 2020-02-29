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
SECONDS = conf.SECONDS(initial=30, cast=int)
TOKEN = conf.TOKEN(initial="")

headers = {"Authorization": f"Token {TOKEN}"}

# clients
app = Celery("ping", include=['ping.tasks',], **CELERY_ARGS)


@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    log.info("setup periodic task {}".format(SECONDS))
    from .tasks import fetch
    app.add_periodic_task(SECONDS * 1.0, fetch.s(), name="every {}".format(SECONDS))




if __name__ == "__main__":
    app.start()
