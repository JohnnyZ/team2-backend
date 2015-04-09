# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

	dependencies = [
		('api', '0005_auto_20150330_1808'),
	]

	operations = [
		migrations.RenameField(
			model_name='appuser',
			old_name='mediation_time',
			new_name='meditation_time',
		),
	]
