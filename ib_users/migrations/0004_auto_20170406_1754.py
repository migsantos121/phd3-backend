# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-06 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_users', '0003_auto_20170406_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField()),
                ('old_val', models.CharField(default=b'', max_length=100)),
                ('new_val', models.CharField(default=b'', max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[(b'EMAIL', b'Email'), (b'PHONE_NO', b'Phone Number'), (b'PASSWORD', b'Password'), (b'USER_NAME', b'Username'), (b'NONE', b'None')], default=b'NONE', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ibuser',
            name='change_history',
            field=models.ManyToManyField(to='ib_users.ChangeHistory'),
        ),
    ]
