# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-18 13:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lhcbpr_api', '0003_auto_20161201_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job', to='lhcbpr_api.AddedResult'),
        ),
    ]
