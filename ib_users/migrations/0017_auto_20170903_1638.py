# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 16:38
from __future__ import unicode_literals

from django.db import migrations
import ib_users.models.ib_user


class Migration(migrations.Migration):

    dependencies = [
        ('ib_users', '0016_auto_20170821_2206'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ibuser',
            managers=[
                ('objects', ib_users.models.ib_user.IBUserManager()),
            ],
        ),
    ]
