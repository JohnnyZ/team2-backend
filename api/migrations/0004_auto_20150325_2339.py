# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
		('api', '0003_auto_20150325_2140'),
	]

	operations = [
		migrations.CreateModel(
			name='ExerciseSession',
			fields=[
				('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
				('exercise_id', models.IntegerField()),
				('percent_completed', models.FloatField()),
				('created_at', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at', editable=False)),
				('updated_at', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='updated_at', editable=False)),
				('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
			],
			options={
			},
			bases=(models.Model,),
		),
		migrations.RemoveField(
			model_name='excercisesession',
			name='user',
		),
		migrations.DeleteModel(
			name='ExcerciseSession',
		),
		migrations.RenameField(
			model_name='appuser',
			old_name='excercise_day_of_week',
			new_name='exercise_day_of_week',
		),
		migrations.RenameField(
			model_name='appuser',
			old_name='excercise_time',
			new_name='exercise_time',
		),
	]
