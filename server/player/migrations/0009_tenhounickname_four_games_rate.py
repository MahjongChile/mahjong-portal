# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-27 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_auto_20180426_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhounickname',
            name='four_games_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
