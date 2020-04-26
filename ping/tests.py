import unittest
from .tasks import ping, dnsbl, run_ping, insert_influxdb
from .tasks import insert_influxdb_bl, InfluxDBClient
from .tasks import run_dnsbl, check_ping
from unittest.mock import patch, MagicMock
from notifiers.core import all_providers
from .providers import Dummy


class TTest(unittest.TestCase):
    def test_check_ping(self):
        check_ping()
    def test_noti(self):
        if not "dummy" in all_providers():
            d = Dummy()
            d.notify(d="shshshs")

@patch("ping.tasks.InfluxDBClient")
class PingTest(unittest.TestCase):
    def test_ping(self, mock_InfluxDBClient):
        result = ping("google.com")
        self.assertTrue("return_code" in result)

    def test_dnsbl(self, mock_InfluxDBClient):
        result = dnsbl("intranet.interalia.net", None)
        self.assertTrue("blacklisted" in result)

    def test_run_ping(self, mock_InfluxDBClient):
        mock_InfluxDBClient.write_points = MagicMock(return_value=True)
        res = run_ping.apply(args=("google.com", "name", 1)).get()
        self.assertTrue(res)
    def test_run_dnsbl(self, mock_InfluxDBClient):
        mock_InfluxDBClient.write_points = MagicMock(return_value=True)
        r =run_dnsbl.apply(args=("intranet.interalia.net", {})).get()
        self.assertTrue(r)
