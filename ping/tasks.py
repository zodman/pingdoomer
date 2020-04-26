from .celery import *
import logging
from pydnsbl import DNSBLChecker
import socket

logging.basicConfig(level=logging.DEBUG)



@app.task
def run_ping(hostname, name, external_id):
    log.info("run_ping({},{},{})".format(hostname, name, external_id))
    influxdb_client = InfluxDBClient(**INFLUXDB_CONF)
    result_stats = ping(hostname)
    return insert_influxdb(influxdb_client, result_stats, name, external_id, hostname)

@app.task
def run_dnsbl(hostname, account):
    log.info(f"run_dnsbl({hostname},{account}")
    result = dnsbl(hostname, account)
    client = InfluxDBClient(**INFLUXDB_CONF)
    return insert_influxdb_bl(client, result, account)

@app.task
def fetch(mode, debug=False):
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
            if host["type"] == "ping" and mode == "ping":
                if debug:
                    run_ping(hostname, name, external_id)
                else:
                    run_ping.delay(hostname, name, external_id)
            if host["type"] == "black" and mode == "blacklist":
                if debug:
                    run_dnsbl(hostname, i)
                else:
                    run_dnsbl.delay(hostname, i)



def insert_influxdb_bl(client, result, account):
    hostname = result.get("hostname")
    name = account.get("name")
    external_id = account.get("external_id")

    fields = {}
    fields=result["result"]
    fields["blacklisted"] = 1 if result["blacklisted"] else 0

    d = {
        "measurement": f"account_{external_id}_bl",
        "tags": {
            "hostname": hostname, 
            "name": name,
            "blacklisted": result["blacklisted"]
        },
        "fields":fields,
    }

    log.debug("write to influxdb {}".format(json.dumps(d, indent=4)))
    return client.write_points([d])


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

def dnsbl(hostname, account):
    result_ip = socket.gethostbyname(hostname)
    log.debug(f"HOSTNAME: {hostname} IP: {result_ip}")
    checker = DNSBLChecker()
    r = checker.check_ip(result_ip)
    log.debug(f"{result_ip} is {r.blacklisted} by {r.detected_by} ")
    dict_result = {}

    providers = [i.host for  i in r.providers ]
    for i in providers:
        dict_result[i] = 0
    for host, result in  r.detected_by.items():
        dict_result[host] = 1
    ds = {
        'blacklisted': r.blacklisted,
        'ip': result_ip,
        'hostname':hostname,
        'detected_by': r.detected_by,
        'providers': providers,
        'result': dict_result
    }
    log.debug(ds)
    return ds

def check_ping():
    influxdb_client = InfluxDBClient(**INFLUXDB_CONF)

if __name__ == "__main__": # pragma: no cover
    log.debug("set debug")
    import sys
    fetch(sys.argv[1], debug=True)
