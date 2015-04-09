# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0009_remove_exercisesession_percent_completed'),
	]

	operations = [
		migrations.AddField(
			model_name='exercisesession',
			name='exercise_id',
			field=models.IntegerField(default=2000),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='meditationsession',
			name='meditation_id',
			field=models.IntegerField(default=1000),
			preserve_default=False,
		),
	]
