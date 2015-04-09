# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0006_auto_20150330_1918'),
	]

	operations = [
		migrations.AlterField(
			model_name='appuser',
			name='exercise_time',
			field=models.TimeField(),
			preserve_default=True,
		),
		migrations.AlterField(
			model_name='appuser',
			name='meditation_time',
			field=models.TimeField(),
			preserve_default=True,
		),
	]
