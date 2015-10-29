# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0004_auto_20150813_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('longitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Logbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('freeFallTime', models.FloatField()),
                ('exitAltitude', models.FloatField()),
                ('deploymentAltitude', models.FloatField()),
                ('maxVerticalVelocity', models.FloatField()),
                ('location', models.ForeignKey(to='sdc_dashboard.Location')),
                ('sessionData', models.ForeignKey(to='sdc_dashboard.SessionData')),
                ('skyDiver', models.ForeignKey(to='sdc_dashboard.SkyDiver')),
            ],
        ),
    ]
