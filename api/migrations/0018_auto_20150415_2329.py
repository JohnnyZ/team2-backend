# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150415_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercisepush',
            old_name='exercse_id',
            new_name='exercise_id',
        ),
    ]
