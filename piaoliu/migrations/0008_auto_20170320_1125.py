# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piaoliu', '0007_auto_20170319_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowbook',
            name='currentBook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piaoliu.Book'),
        ),
        migrations.AlterField(
            model_name='borrowbook',
            name='currentUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piaoliu.User'),
        ),
    ]
