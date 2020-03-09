# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Latency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=100)),
                ('operation_id', models.CharField(max_length=500)),
                ('response_time', models.FloatField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
