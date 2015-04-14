# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150414_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='boolean',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
