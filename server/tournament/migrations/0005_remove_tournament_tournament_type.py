# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 13:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_tournament_tournament_type_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='tournament_type',
        ),
    ]