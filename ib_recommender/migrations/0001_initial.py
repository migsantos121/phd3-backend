# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ib_common.vernacular_utils.vernacular_utilities_class


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('_category', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ib_common.vernacular_utils.vernacular_utilities_class.VernacularUtilitiesClass),
        ),
        migrations.CreateModel(
            name='CategoryVernacularDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('language_name', models.CharField(default=b'ENGLISH', max_length=100)),
                ('v_category', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vernacular_details', to='ib_recommender.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserActionMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('action_id', models.IntegerField()),
                ('weight', models.FloatField()),
                ('article_id', models.IntegerField()),
                ('is_action_considered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserCategoryMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ib_recommender.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserKeywordMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('keyword_id', models.IntegerField()),
                ('interest_score', models.FloatField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('user_category_map', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ib_recommender.UserCategoryMap')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='useractionmap',
            unique_together=set([('user_id', 'action_id', 'article_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='userkeywordmap',
            unique_together=set([('user_id', 'keyword_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercategorymap',
            unique_together=set([('user_id', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='categoryvernaculardetails',
            unique_together=set([('category', 'language_name')]),
        ),
    ]
