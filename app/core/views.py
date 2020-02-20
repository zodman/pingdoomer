from django.shortcuts import render
from .serializers import AccountSerializer, HostSerializer
from rest_framework import viewsets
from .models import Account, Host


class AccountViewset(viewsets.ModelViewSet):
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

