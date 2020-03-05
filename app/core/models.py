from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=True)



class Account(models.Model):
    name = models.CharField(max_length=100)
    external_id = models.PositiveIntegerField(unique=True)


    def __str__(self):
        return self.name

PING="ping"
BLACKLIST="black"

class Host(models.Model):
    MONITOR_CHOICES = (
        (PING, "ping"),
        (BLACKLIST, "blacklist"),
    )
    hostname = models.CharField(max_length=100)
    type = models.CharField(max_length=5, choices=MONITOR_CHOICES, default=PING)
    account = models.ForeignKey("Account", related_name="hosts",
                                on_delete=models.CASCADE)


    class Meta:
        unique_together =("hostname", "account", "type")

    def __str__(self):
        return self.hostname


class Alert(models.Model):
    options = models.TextField()
    host = models.ForeignKey("Host", related_name="alerts", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

