# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 13:38
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations
import ib_users.models.ib_user


class Migration(migrations.Migration):

    dependencies = [
        ('ib_users', '0017_auto_20170903_1638'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ibuser',
            managers=[
                ('objects', ib_users.models.ib_user.IBUserManager()),
                ('all_objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
