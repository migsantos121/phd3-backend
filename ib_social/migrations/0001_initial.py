# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MemberRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('m_id', models.IntegerField()),
                ('m_type', models.CharField(max_length=255)),
                ('r_m_id', models.IntegerField()),
                ('r_m_type', models.CharField(max_length=255)),
                ('relation', models.CharField(choices=[(b'FRIEND', b'Friend'), (b'FB_FRIEND', b'Facebook Friend'), (b'FOLLOW', b'Following')], default=b'FRIEND', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
