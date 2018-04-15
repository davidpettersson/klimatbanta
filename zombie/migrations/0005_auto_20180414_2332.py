# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-14 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zombie', '0004_travelentry_travel_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentry',
            name='dish_type',
            field=models.CharField(choices=[('M', 'kött'), ('F', 'fisk'), ('V', 'vegetariskt')], max_length=1, verbose_name='dish type'),
        ),
    ]
