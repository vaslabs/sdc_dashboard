# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0003_sharelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharelink',
            name='shareLink',
            field=models.CharField(unique=True, max_length=16),
        ),
    ]
