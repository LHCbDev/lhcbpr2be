# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-04 10:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResultFileSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobresult_ptr_id', models.IntegerField()),
                ('data', models.TextField()),
            ],
            options={
                'db_table': 'lhcbpr_api_resultfile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResultFloatSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobresult_ptr_id', models.IntegerField()),
                ('data', models.TextField()),
            ],
            options={
                'db_table': 'lhcbpr_api_resultfloat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResultIntegerSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobresult_ptr_id', models.IntegerField()),
                ('data', models.TextField()),
            ],
            options={
                'db_table': 'lhcbpr_api_resultinteger',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResultStringSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobresult_ptr_id', models.IntegerField()),
                ('data', models.TextField()),
            ],
            options={
                'db_table': 'lhcbpr_api_resultstring',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AddedResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=64)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('vtime', models.DateTimeField(null=True)),
                ('is_nightly', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='lhcbpr_api.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=512)),
                ('dtype', models.CharField(choices=[(b'String', b'String'), (b'Float', b'Float'), (b'Integer', b'Integer'), (b'DateTime', b'DateTime'), (b'File', b'File')], max_length=10)),
                ('description', models.CharField(max_length=500)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeThreshold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('down_value', models.FloatField()),
                ('up_value', models.FloatField()),
                ('start', models.DateTimeField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thresholds', to='lhcbpr_api.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HandlerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_success', models.BooleanField(default=False)),
                ('old_id', models.IntegerField(null=True)),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhcbpr_api.Handler')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50)),
                ('cpu_info', models.CharField(max_length=200)),
                ('memory_info', models.CharField(max_length=200)),
                ('old_id', models.IntegerField(db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('is_success', models.BooleanField(default=False)),
                ('old_id', models.IntegerField(null=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job', to='lhcbpr_api.Host')),
            ],
        ),
        migrations.CreateModel(
            name='JobDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.IntegerField(null=True)),
                ('application_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='lhcbpr_api.ApplicationVersion')),
            ],
        ),
        migrations.CreateModel(
            name='JobHandler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.IntegerField(null=True)),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhcbpr_api.Handler')),
                ('job_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhcbpr_api.JobDescription')),
            ],
        ),
        migrations.CreateModel(
            name='JobResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('description', models.CharField(max_length=2000)),
                ('is_standalone', models.BooleanField(default=False)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmtconfig', models.CharField(max_length=100, unique=True)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestedPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.IntegerField(null=True)),
                ('cmtconfig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhcbpr_api.Platform')),
                ('job_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='lhcbpr_api.JobDescription')),
            ],
        ),
        migrations.CreateModel(
            name='SetupProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('old_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResultFile',
            fields=[
                ('jobresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lhcbpr_api.JobResult')),
                ('data', models.FileField(upload_to=b'')),
            ],
            bases=('lhcbpr_api.jobresult',),
        ),
        migrations.CreateModel(
            name='ResultFloat',
            fields=[
                ('jobresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lhcbpr_api.JobResult')),
                ('data', models.FloatField()),
            ],
            bases=('lhcbpr_api.jobresult',),
        ),
        migrations.CreateModel(
            name='ResultInteger',
            fields=[
                ('jobresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lhcbpr_api.JobResult')),
                ('data', models.IntegerField()),
            ],
            bases=('lhcbpr_api.jobresult',),
        ),
        migrations.CreateModel(
            name='ResultString',
            fields=[
                ('jobresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lhcbpr_api.JobResult')),
                ('data', models.TextField()),
            ],
            bases=('lhcbpr_api.jobresult',),
        ),
        migrations.AddField(
            model_name='jobresult',
            name='attr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobresults', to='lhcbpr_api.Attribute'),
        ),
        migrations.AddField(
            model_name='jobresult',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='lhcbpr_api.Job'),
        ),
        migrations.AddField(
            model_name='jobdescription',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='lhcbpr_api.Option'),
        ),
        migrations.AddField(
            model_name='jobdescription',
            name='setup_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='lhcbpr_api.SetupProject'),
        ),
        migrations.AddField(
            model_name='job',
            name='job_description',
            field=models.ForeignKey(db_column=b'job_description_id', on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='lhcbpr_api.JobDescription'),
        ),
        migrations.AddField(
            model_name='job',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='lhcbpr_api.Platform'),
        ),
        migrations.AddField(
            model_name='handlerresult',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lhcbpr_api.Job'),
        ),
        migrations.AddField(
            model_name='attributethreshold',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thresholds', to='lhcbpr_api.Option'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='groups',
            field=models.ManyToManyField(related_name='attributes', to='lhcbpr_api.AttributeGroup'),
        ),
        migrations.AddField(
            model_name='applicationversion',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='lhcbpr_api.Slot'),
        ),
        migrations.AlterUniqueTogether(
            name='requestedplatform',
            unique_together=set([('job_description', 'cmtconfig')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobhandler',
            unique_together=set([('job_description', 'handler')]),
        ),
        migrations.AlterUniqueTogether(
            name='applicationversion',
            unique_together=set([('application', 'version')]),
        ),
    ]
