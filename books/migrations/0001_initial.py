# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-16 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('book_type', models.CharField(max_length=2)),
                ('book_sub_type', models.CharField(max_length=4)),
                ('book_name', models.CharField(max_length=30)),
                ('book_url', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=20)),
                ('total_words', models.IntegerField(blank=True, null=True)),
                ('click_count', models.IntegerField(blank=True, null=True)),
                ('recommand_count', models.IntegerField(blank=True, null=True)),
                ('book_status', models.CharField(max_length=2)),
                ('rank_score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('rank_ppl_involved', models.IntegerField(blank=True, null=True)),
                ('last_upload_date', models.DateTimeField()),
                ('last_update_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'qidian',
            },
        ),
    ]