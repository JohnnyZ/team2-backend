# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0007_auto_20150330_2157'),
	]

	operations = [
		migrations.RemoveField(
			model_name='exercisesession',
			name='exercise_id',
		),
		migrations.RemoveField(
			model_name='meditationsession',
			name='meditation_id',
		),
	]
