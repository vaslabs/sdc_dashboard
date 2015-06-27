# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0002_auto_20150621_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shareLink', models.CharField(max_length=16)),
                ('expires', models.DateTimeField(verbose_name=b'date expires')),
                ('userShared', models.ForeignKey(to='sdc_dashboard.SkyDiver')),
            ],
        ),
    ]
