# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_users', '0008_auto_20170411_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersocialprovider',
            name='social_id',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='usersocialprovider',
            name='social_name',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
