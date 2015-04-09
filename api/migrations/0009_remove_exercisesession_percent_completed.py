# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0008_auto_20150330_2203'),
	]

	operations = [
		migrations.RemoveField(
			model_name='exercisesession',
			name='percent_completed',
		),
	]
