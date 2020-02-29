from django.shortcuts import render, get_object_or_404
from .serializers import AccountSerializer, HostSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Account, Host, PING, BLACKLIST
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from influxdb import InfluxDBClient
import json
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class AccountViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class HostViewset(viewsets.ModelViewSet):
    serializer_class = HostSerializer

    def get_queryset(self):
        return Host.objects.filter(account=self.kwargs['accounts_pk'])

    def perform_update(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])

    def perform_create(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])

    def _ping(self, host):
        influx_conf = settings.PING_CONFIG["INFLUXDB"]
        client = InfluxDBClient(**influx_conf)
        external_id = host.account.external_id
        hostname = host.hostname
        sql_all =f"""
        select * 
                FROM "ping"."autogen"."account_{external_id}" 
                     WHERE time > now() - 7d 
                     AND "hostname"='{hostname}' limit 50
        """
        sql = f"""
            Select * from (
            SELECT 
                count("rtt_avg") AS "count_rtt_avg", 
                mean("rtt_avg") AS "mean_rtt_avg"
                FROM "ping"."autogen"."account_{external_id}" 
                     WHERE time > now() - 30d 
                     AND "hostname"='{hostname}'
                     GROUP BY time(10m)

                    ) where "count_rtt_avg" > 0  
        """
        res = {
            'all': list(client.query(sql_all).get_points()),
            'summary': list(client.query(sql).get_points())
        }
        return Response(res)
    def _blacklist(self, host):

        influx_conf = settings.PING_CONFIG["INFLUXDB"]
        client = InfluxDBClient(**influx_conf)
        external_id = host.account.external_id
        hostname = host.hostname
        sql = f"""
        SELECT  *
            FROM "ping"."autogen"."account_{external_id}_bl" 
            WHERE time > now() -  7d
            AND time < now() 
            AND  "hostname"='{hostname}'
            limit 30
        """
        res = list(client.query(sql).get_points())
        return Response(res)
    # @method_decorator(cache_page(10))
    def retrieve(self, request, pk=None, accounts_pk=None):
        qs = Host.objects.all().filter(account_id= accounts_pk)
        host = get_object_or_404(qs, pk=pk)
        if host.type == PING:
            return self._ping(host)
        if host.type == BLACKLIST:
            return self._blacklist(host)
