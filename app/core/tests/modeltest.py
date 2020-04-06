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
        data = {
            'name': self.faker.first_name(),
            'external_id': self.faker.pyint(),
            'options': json.dumps([{
                'notifier': 'email',
                'options': {
                    'subject': "New email from 'notifiers'!",
                    'from': 'zodman@aUTOMATION.localdomain',
                    'host': 'localhost',
                    'port': 25,
                    'tls': False,
                    'ssl': False,
                    'html': False,
                    'login': True
                },
            }, {
                'notifier': 'slack',
                'options': slack_notifier.defaults,
            }])
        }
        resp = Account(**data)
        resp.full_clean()
        resp.save()
