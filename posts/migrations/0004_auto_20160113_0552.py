# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 10:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160113_0458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at', '-updated_at']},
        ),
    ]
