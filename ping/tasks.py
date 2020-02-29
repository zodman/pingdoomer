from .celery import *
import logging


logging.basicConfig(level=logging.DEBUG)



@app.task
def run_ping(hostname, name, external_id):
    log.info("run_ping({},{},{})".format(hostname, name, external_id))
    influxdb_client = InfluxDBClient(**INFLUXDB_CONF)
    result_stats = ping(hostname)
    return insert_influxdb(influxdb_client, result_stats, name, external_id, hostname)


@app.task
def fetch(debug=False):
    log.info("executing fetch")
    base_url = f"{BASE_URL}api/accounts/"
    resp = requests.get(base_url, headers=headers)
    resp.raise_for_status()
    resp = resp.json()
    for i in resp:
        external_id = i.get("external_id")
        name = i.get("name")
        id = i.get("id")
        hosts = requests.get(f"{base_url}{id}/hosts/").json()
        for host in hosts:
            hostname = host["hostname"]
            if debug:
                run_ping(hostname, name, external_id)
            else:
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
    fetch(debug=True)
