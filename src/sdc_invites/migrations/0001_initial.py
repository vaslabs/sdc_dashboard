# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_dashboard', '0007_logbook_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdDate', models.DateTimeField(verbose_name=b'date submitted')),
                ('expiresDate', models.DateTimeField(verbose_name=b'date expires')),
                ('token', models.CharField(unique=True, max_length=16)),
                ('numberOfInvitesAllowed', models.IntegerField()),
                ('numberOfInvitesTaken', models.IntegerField()),
                ('skydiver', models.ForeignKey(to='sdc_dashboard.SkyDiver')),
            ],
        ),
    ]
