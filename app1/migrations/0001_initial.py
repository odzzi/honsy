# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-08 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=256)),
                ('type_name', models.CharField(max_length=256)),
                ('row_id', models.CharField(max_length=256)),
                ('row_value', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'honsy_meta',
            },
        ),
    ]
