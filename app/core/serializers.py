from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField as Related
from .models import Account, Host,  Alert


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alert
        fields = ("options", "active", "id")


class HostSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'accounts_pk': 'account__pk',
        'host_pk': 'hosts__pk'
    }
    alerts = Related(many=True,
                     read_only=True,
                     view_name='alerts-detail',
                     parent_lookup_kwargs={
                         'accounts_pk': 'account__pk',
                         'hosts_pk': 'host__pk'
                     })

    class Meta:
        model = Host
        fields = ("id", "hostname", "type", "alerts")
        #TODO validation unique_toguether


class AAAHostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account-hosts-detail")

    class Meta:
        model = Host
        fields = "__all__"


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    hosts = Related(many=True,
                    read_only=True,
                    view_name='account-hosts-detail',
                    parent_lookup_kwargs={'accounts_pk': 'account__pk'})

    class Meta:
        model = Account
        fields = ("id", "name", "external_id", "hosts")
