
import faker
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
import django
django.setup()
from core.models import *

account, _ = Account.objects.get_or_create(name="default", external_id=123)

HOSTS = [
    ("google.com", "ping"),
    ("intranet.interalia.net", "ping"),
    ("intranet.interalia.net", "black"),
    ("kiakonfidence.mx", "black"),
]
fake = faker.Faker()

contact, _ = Contact.objects.get_or_create(account=account, 
                                  name=fake.first_name(), 
                                  phone=fake.phone_number(),
                                  email="pingdoomer@tempemailaddress.com"
                                  )

Alert.objects.all().delete()

options = """
{'type':''}
"""

for host, type in HOSTS:
    host_obj, _ = Host.objects.get_or_create(account=account, type=type, hostname=host)
    a,_ = Alert.objects.get_or_create(account=account, host=host_obj, options=options)
    a.contacts.add(contact)


