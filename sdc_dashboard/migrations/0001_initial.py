# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SessionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submittedDate', models.DateTimeField(verbose_name=b'date submitted')),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SkyDiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='sessiondata',
            name='skyDiver',
            field=models.ForeignKey(to='sdc_dashboard.SkyDiver'),
        ),
    ]
