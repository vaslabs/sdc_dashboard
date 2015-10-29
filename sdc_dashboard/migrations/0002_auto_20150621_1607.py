# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skydiver',
            name='username',
            field=models.CharField(default=datetime.datetime(2015, 6, 21, 16, 7, 10, 524710, tzinfo=utc), unique=True, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skydiver',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
