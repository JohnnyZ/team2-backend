# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
from django.conf import settings
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name='appUser',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('password', models.CharField(max_length=128, verbose_name='password')),
				('birthday', models.DateField(blank=True, null=True)),
				('gender', models.IntegerField(default=0)),
				('start_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
				('mediation_time', models.DateTimeField()),
				('excercise_day_of_week', models.IntegerField(default=0)),
				('excercise_time', models.DateTimeField()),
				('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='created_at')),
				('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='updated_at')),
				('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
			],
			options={
			},
			bases=(models.Model,),
		),
		migrations.CreateModel(
			name='ExcerciseSession',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('Excercise_id', models.IntegerField()),
				('percent_completed', models.FloatField()),
				('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='created_at')),
				('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='updated_at')),
				('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
			],
			options={
			},
			bases=(models.Model,),
		),
		migrations.CreateModel(
			name='MeditationSession',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('meditation_id', models.IntegerField()),
				('percent_completed', models.FloatField()),
				('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='created_at')),
				('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False, verbose_name='updated_at')),
				('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
			],
			options={
			},
			bases=(models.Model,),
		),
	]
