# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-28 16:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('third_app', '0011_poke'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poke',
            name='poke',
        ),
    ]
