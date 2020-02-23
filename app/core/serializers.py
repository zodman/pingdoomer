from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Account, Host


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('id','hostname')
        #TODO validation unique_toguether




class AccountSerializer(serializers.HyperlinkedModelSerializer):
    hosts = HostSerializer(many=True)
    class Meta:
        model = Account
        fields = ("id", "name", "external_id", "hosts")

