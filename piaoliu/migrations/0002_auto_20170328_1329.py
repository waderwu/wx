# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piaoliu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
