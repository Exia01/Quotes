# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-23 22:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xapp', '0029_auto_20180523_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='adder',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='poster',
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
