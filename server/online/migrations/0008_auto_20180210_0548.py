# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-10 05:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0007_tournamentstatus_registration_closed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tournamentgame',
            options={'ordering': ['-tournament_round', 'status', 'tournament']},
        ),
    ]
