# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django_extensions.db.fields
import django.utils.timezone


class Migration(migrations.Migration):

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
		('api', '0011_auto_20150407_1922'),
	]

	operations = [
		migrations.CreateModel(
			name='UserProfile',
			fields=[
				('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
				('birthday', models.DateField(null=True, blank=True)),
				('gender', models.IntegerField(default=0)),
				('start_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
				('meditation_time', models.TimeField()),
				('exercise_day_of_week', models.IntegerField(default=0)),
				('exercise_time', models.TimeField()),
				('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created_at', editable=False, blank=True)),
				('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='updated_at', editable=False, blank=True)),
				('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
			],
			options={
			},
			bases=(models.Model,),
		),
		migrations.RemoveField(
			model_name='appuser',
			name='user',
		),
		migrations.DeleteModel(
			name='appUser',
		),
	]
