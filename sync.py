from ping.tasks import fetch_accounts
from ping.celery import InfluxDBClient, INFLUXDB_CONF


client = InfluxDBClient(**INFLUXDB_CONF)

results = client.query("show measurements;")

list_measures = []
for res in results:
    for r in res:
        list_measures.append(r.get("name"))

res = fetch_accounts()
for r in res:
    list_measures.remove(f"account_{r}")

for  r  in list_measures:
    sql =f'drop measurement {r}'
    print(sql)
    client.query(sql)


