# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-01 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lhcbpr_api', '0002_auto_20160419_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultJSON',
            fields=[
                ('jobresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lhcbpr_api.JobResult')),
                ('data', models.TextField()),
            ],
            bases=('lhcbpr_api.jobresult',),
        ),
        migrations.RemoveField(
            model_name='option',
            name='executable',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='dtype',
            field=models.CharField(choices=[(b'String', b'String'), (b'JSON', b'JSON'), (b'Float', b'Float'), (b'Integer', b'Integer'), (b'DateTime', b'DateTime'), (b'File', b'File')], max_length=10),
        ),
        migrations.AlterField(
            model_name='jobdescription',
            name='executable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='lhcbpr_api.Executable'),
        ),
    ]