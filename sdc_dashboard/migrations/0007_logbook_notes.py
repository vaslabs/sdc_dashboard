# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0006_logbook_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbook',
            name='notes',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
