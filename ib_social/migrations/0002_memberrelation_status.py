# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberrelation',
            name='status',
            field=models.CharField(choices=[(b'ACCEPTED', b'Accepted'), (b'PENDING', b'Pending'), (b'REJECTED', b'Rejected')], default=b'PENDING', max_length=100),
        ),
    ]
