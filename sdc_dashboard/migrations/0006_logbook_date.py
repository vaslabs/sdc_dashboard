# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0005_location_logbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbook',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 22, 10, 26, 36, 559272, tzinfo=utc), verbose_name=b'date of session'),
            preserve_default=False,
        ),
    ]
