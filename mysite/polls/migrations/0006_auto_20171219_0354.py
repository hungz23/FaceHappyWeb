# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-19 03:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20171219_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotion',
            name='date',
            field=models.DateTimeField(default=datetime.date(2017, 12, 19)),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.date(2017, 12, 19)),
        ),
    ]