
import unittest
from .tasks import ping, dnsbl, run_ping, insert_influxdb, insert_influxdb_bl, InfluxDBClient
from .tasks import run_dnsbl
from unittest.mock import patch, MagicMock

import logging
logging.disable(logging.CRITICAL)


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
        

