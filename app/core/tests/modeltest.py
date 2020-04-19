from django.test import TestCase
import faker
from core.models import Account
import json
from notifiers import get_notifier


class ModelTestCase(TestCase):
    def setUp(self):
        self.faker = faker.Faker()

    def test_account(self):
        email_notifier = get_notifier("email")
        slack_notifier = get_notifier("slack")
        opts = slack_notifier.defaults.copy()
        opts.update({'message':'message1','webhook_url':'http://localhost'})
        data = {
            'name': self.faker.first_name(),
            'external_id': self.faker.pyint(),
            'options': json.dumps([{
                'provider': 'email',
                'options': {
                    'username': 'user1',
                    'password': 'user1',
                    'subject': "New email from 'notifiers'!",
                    'from': 'zodman@aUTOMATION.localdomain',
                    'host': 'localhost',
                    'port': 25,
                    'to': ['nobody@email.com',],
                    'message': 'msg default',
                },
            }, {
                'provider': 'slack',
                'options': opts,
            }])
        }
        resp = Account(**data)
        resp.full_clean()
        resp.save()
