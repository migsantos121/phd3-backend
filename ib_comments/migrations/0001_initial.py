# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('entity_id', models.IntegerField()),
                ('entity_type', models.CharField(max_length=100)),
                ('user_id', models.IntegerField()),
                ('comment', models.CharField(max_length=400)),
                ('up_votes', models.IntegerField(default=0)),
                ('down_votes', models.IntegerField(default=0)),
                ('multimedia_url', models.CharField(blank=True, max_length=500, null=True)),
                ('multimedia_type', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCommentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ib_comments.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='UserCommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField()),
                ('vote', models.CharField(choices=[(b'UP_VOTE', b'UP_VOTE'), (b'DOWN_VOTE', b'DOWN_VOTE'), (b'NEUTRAL', b'NEUTRAL')], max_length=30)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ib_comments.Comment')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usercommentvote',
            unique_together=set([('user_id', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercommentreport',
            unique_together=set([('user_id', 'comment')]),
        ),
    ]
