# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-14 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zombie', '0005_auto_20180414_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelentry',
            name='geometry',
            field=models.TextField(default='', verbose_name='geometry'),
            preserve_default=False,
        ),
    ]
