from django.db import models
from django.core.exceptions import ValidationError
import json
from jsonschema import validate
from notifiers import get_notifier
import notifiers.exceptions
import logging

log = logging.getLogger(__name__)

def validate_options(opts):
    python_objs = json.loads(opts)
    if not isinstance(python_objs, list):
        raise ValidationError("error [{'provider':'name', 'options': ..}, ...]")
    for i in python_objs:
        log.info(i)
        if not isinstance(i, dict):
            raise ValidationError(" {'provider':'name', 'options': ..}")
        notifier_provider = i.get("provider")
        options = i.get("options")
        provider = get_notifier(notifier_provider)
        if provider:
            try:
                provider._process_data(**options)
            except notifiers.exceptions.BadArguments as e:
                raise ValidationError(f"provider {provider.name} {e}")
        else:
            raise ValidationError(f"no provider by {i}")

class Account(models.Model):
    name = models.CharField(max_length=100)
    external_id = models.PositiveIntegerField(unique=True)
    options = models.TextField(validators=[validate_options], null=False, blank=False)

    def __str__(self):
        return self.name

from django.dispatch import receiver
from django.db.models.signals import post_delete

@receiver(post_delete)
def delete_messurage(sender, instance, **kwargs):
    from influxdb import InfluxDBClient
    from django.conf import settings
    external_id = instance.external_id
    client = InfluxDBClient(**settings.PING_CONFIG.get("INFLUXDB",{}))
    sql =f'drop measurement  account_{external_id}'
    res = client.query(sql)

PING = "ping"
BLACKLIST = "black"


class Host(models.Model):
    MONITOR_CHOICES = (
        (PING, "ping"),
        (BLACKLIST, "blacklist"),
    )
    hostname = models.CharField(max_length=100)
    type = models.CharField(max_length=5,
                            choices=MONITOR_CHOICES,
                            default=PING)
    account = models.ForeignKey("Account",
                                related_name="hosts",
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = ("hostname", "account", "type")

    def __str__(self):
        return self.hostname


class Alert(models.Model):
    options = models.TextField()
    host = models.ForeignKey("Host",
                             related_name="alerts",
                             on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
