from django.shortcuts import render, get_object_or_404
from .serializers import AccountSerializer, HostSerializer, ContactSerailizer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Account, Host, PING, BLACKLIST, Contact
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from influxdb import InfluxDBClient
import json
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action


class ConcactViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerailizer
    queryset = Contact.objects.all()

    def perform_update(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])

    def perform_create(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])


class AccountViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class HostViewset(viewsets.ModelViewSet):
    serializer_class = HostSerializer

    def get_queryset(self):
        hosts = Host.objects.filter(account=self.kwargs['accounts_pk'])
        return hosts

    def perform_update(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])

    def perform_create(self, serializer):
        serializer.save(account_id = self.kwargs["accounts_pk"])

    # @method_decorator(cache_page(10))
    @action(detail=True)
    def result(self, request, pk=None, accounts_pk=None):
        qs = Host.objects.all().filter(account_id= accounts_pk)
        host = get_object_or_404(qs, pk=pk)
        if host.type == PING:
            return self._ping(host)
        if host.type == BLACKLIST:
            return self._blacklist(host)

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
            SELECT last("blacklisted") AS "last_blacklisted" 
            FROM "ping"."autogen"."account_{external_id}_bl"
            WHERE time > now() - 7d AND time < now() 
            and "hostname"='{hostname}'
            GROUP BY time(1m), "hostname" 
            FILL(0)  
            order by time asc
            limit 1

        """
        res = list(client.query(sql).get_points())
        
        sql = f"""
        SELECT * FROM "ping"."autogen"."account_{external_id}_bl" 
        WHERE time > now() -7d
            AND time < now()
            AND "hostname"='{hostname}' 
            order by time desc
            limit 1
        """
        res2 = list(client.query(sql).get_points())
        return Response({'last': res, 'all':res2})


