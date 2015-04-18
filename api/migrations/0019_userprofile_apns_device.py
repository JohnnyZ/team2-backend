# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0002_auto_20150417_2029'),
        ('api', '0018_auto_20150415_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='apns_device',
            field=models.ForeignKey(blank=True, to='push_notifications.APNSDevice', null=True),
            preserve_default=True,
        ),
    ]
