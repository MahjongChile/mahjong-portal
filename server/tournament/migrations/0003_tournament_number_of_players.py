# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-16 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20171216_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='number_of_players',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
