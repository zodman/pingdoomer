from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    external_id = models.PositiveIntegerField(unique=True)


    def __str__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=100)
    account = models.ForeignKey("Account", related_name="hosts",
                                on_delete=models.CASCADE)


    class Meta:
        unique_together =("hostname", "account")

    def __str__(self):
        return self.hostname
