# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_users', '0005_auto_20170407_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userotp',
            name='reset_count',
        ),
        migrations.AddField(
            model_name='userotp',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
