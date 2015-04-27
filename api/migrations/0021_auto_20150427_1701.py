# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_exercisereminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentpush',
            name='assessment',
            field=models.ForeignKey(default=0, to='api.Assessment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessmentpush',
            name='is_momentary',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
