# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150414_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='complete_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assessment',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='response',
            name='number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
