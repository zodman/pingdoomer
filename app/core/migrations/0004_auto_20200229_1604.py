# Generated by Django 3.0.3 on 2020-02-29 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_host_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='host',
            unique_together={('hostname', 'account', 'type')},
        ),
    ]
