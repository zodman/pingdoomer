# Generated by Django 3.0.3 on 2020-04-06 04:15

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200406_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='options',
        ),
        migrations.AddField(
            model_name='account',
            name='options',
            field=models.TextField(default='', validators=[core.models.validate_options]),
            preserve_default=False,
        ),
    ]
