from django.shortcuts import render, get_object_or_404
from .serializers import AccountSerializer, HostSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Account, Host
from rest_framework.permissions import IsAuthenticated



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


    def retrieve(self, request, pk=None, accounts_pk=None):
        qs = Host.objects.all().filter(account_id= accounts_pk)
        host = get_object_or_404(qs, pk=pk)

        return Response("")

