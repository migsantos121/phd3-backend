# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-02 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_articles', '0006_auto_20170702_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='_author_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='article',
            name='_url',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='articlevernaculardetails',
            name='v_author_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='articlevernaculardetails',
            name='v_url',
            field=models.CharField(max_length=600),
        ),
    ]
