from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from rest_framework_nested.relations import NestedHyperlinkedRelatedField


from .models import Account, Host, Contact


class ContactSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"



class HostSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs={'accounts_pk': 'account__pk'}

    class Meta:
        model = Host
        fields = ("id", "hostname", "type")
        #TODO validation unique_toguether

class AAAHostSerializer(serializers.HyperlinkedModelSerializer):
    #accounts = AccountHostSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="account-hosts-detail")

    class Meta:
        model = Host
        fields = "__all__"

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    contacts = NestedHyperlinkedRelatedField(
                many=True,
                read_only=True,
                view_name='account-contacts-detail',
                parent_lookup_kwargs={'accounts_pk': 'account__pk'}
            )

    hosts = NestedHyperlinkedRelatedField(
                many=True,
                read_only=True,
                view_name='account-hosts-detail',
                parent_lookup_kwargs={'accounts_pk': 'account__pk'}
            )
    class Meta:
        model = Account
        fields = ("id", "name", "external_id", "hosts", "contacts")

