from django.shortcuts import render, get_object_or_404
from .serializers import AccountSerializer, HostSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Account, Host
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

    # @method_decorator(cache_page(10))
    def retrieve(self, request, pk=None, accounts_pk=None):
        qs = Host.objects.all().filter(account_id= accounts_pk)
        host = get_object_or_404(qs, pk=pk)
        influx_conf = settings.PING_CONFIG["INFLUXDB"]
        client = InfluxDBClient(**influx_conf)
        external_id = host.account.external_id
        hostname = host.hostname
        result = client.query(f"""
            SELECT *
                     FROM "ping"."autogen"."account_{external_id}" 
                     WHERE time > now() - 7d 
                     AND "hostname"='{hostname}'
                    """)
        res = list(result.get_points())
        return Response(res)

