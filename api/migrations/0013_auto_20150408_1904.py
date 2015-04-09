# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0012_auto_20150408_1821'),
	]

	operations = [
		migrations.AlterField(
			model_name='userprofile',
			name='exercise_time',
			field=models.TimeField(null=True),
			preserve_default=True,
		),
		migrations.AlterField(
			model_name='userprofile',
			name='meditation_time',
			field=models.TimeField(null=True),
			preserve_default=True,
		),
	]
