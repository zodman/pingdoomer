from rest_framework.authtoken.models import Token
from test_plus import APITestCase
import faker
import json
from django_seed import Seed
from core.models import Account, Host, Alert
from notifiers import get_notifier
import os

class TestAlert(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = self.make_user("user1")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.faker = faker.Faker()

        data = {
            'name': self.faker.first_name(),
            'external_id': self.faker.pyint(),
            'options': json.dumps([{
                'provider': 'telegram',
                'options': {
                    'token': "12321321321",
                    'chat_id': '1321321',
                    'message':'message1'
                }
            }])
        }

        self.account = Account(**data)
        self.account.full_clean()
        self.account.save()
        self.host = Host.objects.create(hostname="google.com", type="ping",account=self.account)
        opts = json.dumps({
            'provider': 'telegram',
            'options': {
                'message': 'YEH!!!'
            }
        })
        self.alert = Alert.objects.create(account=self.account, host=self.host, options=opts)

    def test_provider(self):
        default_options = json.loads(self.alert.account.options)
        act_opt = json.loads(self.alert.options)
        for doptions in default_options:
            provider_name = doptions.get("provider")
            opts = doptions.get("options")
            action_provider_name = act_opt.get("provider")
            action_options = act_opt.get("options")
            notify = get_notifier(provider_name)
            opts.update(action_options)
            notify._process_data(**opts)

            


