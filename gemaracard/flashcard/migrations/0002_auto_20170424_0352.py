# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='translation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='language',
            field=models.CharField(choices=[('HEB', 'Hebrew'), ('ARAM', 'Aramaic'), ('LW', 'Loanword')], default='HEB', max_length=4),
        ),
    ]