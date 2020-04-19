# Pingdoomer

## django ping monitor and blacklist



### Models

```python
class Account(models.Model):
    name = fields.CharField()
    externa_id = fields.IntegerField()
    
class Host(models.Model)
    hostname = fields.CharField()
    account = fields.ForeignKey()
```

### Django rest framework

    - POST create
    - PUT update
    - DEL delete

#### Api (protected by Apikey for writing and other for reading):

    v1/api/account/
    v1/api/account/<account_id>/hosts/
    v1/api/account/<account_id>/hosts/<host_id>/
        - GET for obtain all data to graph. and last result





### TimeserieDB:: InfluxDB

I will store the ping stats using [pingparsing](https://pypi.org/project/pingparsing/) into a [influxdb](https://github.com/influxdata/influxdb-python)

```python=
$ python
>>> from influxdb import InfluxDBClient
>>> json_body = [
    {
        "measurement": "account_<external_id>",
        "tags": {
            "hostname": "<hostname>",
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "packet_transmit": 10,
            "packet_receive": 10,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 34.189,
            "rtt_avg": 46.054,
            "rtt_max": 63.246,
            "rtt_mdev": 9.122,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0

        }
    }
]
>>> client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
>>> client.create_database('example')
>>> client.write_points(json_body)
>>> result = client.query('select * from account_<slug> group by hostname;')
>>> print("Result: {0}".format(result))
```


### Celery tasks

- scheduler()
    - Obtain all host and throw everything to workers

- run(account__name, host)
    - execute the ping on host
    - parse the ping stats
    - insert into influxdb

Celery workers to execute the ping and a celery scheduler to execute each time needed.


### commands to add

```
 pip install httpie
 http POST localhost:8000/api/accounts/ 'Authorization:Token <token>' name=andres1 external_id=10
 http POST localhost:8000/api/accounts/6/hosts/ 'Authorization:Token <token>' hostname=waifu.ca
```




