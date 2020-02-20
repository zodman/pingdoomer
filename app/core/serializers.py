from rest_framework import serializers
from .models import Account, Host

class AccountSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Account
        fields = "__all__"

class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = "__all__"


