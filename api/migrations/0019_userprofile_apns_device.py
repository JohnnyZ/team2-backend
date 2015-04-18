# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
from django.conf import settings
from push_notifications import *


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0002_auto_20150417_2029'),
        ('api', '0018_auto_20150415_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='apns_device',
            field=models.ForeignKey(default=0, to='push_notifications.APNSDevice'),
            preserve_default=False,
        ),
    ]
