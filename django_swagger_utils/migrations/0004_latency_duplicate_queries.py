# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_swagger_utils', '0003_auto_20161102_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='latency',
            name='duplicate_queries',
            field=models.IntegerField(default=0),
        ),
    ]
