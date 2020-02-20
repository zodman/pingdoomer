from rest_framework import serializers
from .models import Account, Host


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('id','hostname', 'account')

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    hosts = HostSerializer(many=True)
    class Meta:
        model = Account
        fields = ("id", "name", "external_id", "hosts")

