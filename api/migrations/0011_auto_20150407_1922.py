# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0010_auto_20150401_1625'),
	]

	operations = [
		migrations.AlterUniqueTogether(
			name='exercisesession',
			unique_together=set([('user', 'exercise_id')]),
		),
	]
