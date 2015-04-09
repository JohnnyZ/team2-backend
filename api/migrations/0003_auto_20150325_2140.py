# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0002_remove_appuser_password'),
	]

	operations = [
		migrations.RenameField(
			model_name='excercisesession',
			old_name='Excercise_id',
			new_name='excercise_id',
		),
	]
