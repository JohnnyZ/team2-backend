# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0016_auto_20150414_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentPush',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('next_send', models.DateTimeField()),
                ('sent', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'created_at', editable=False, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExercisePush',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'created_at', editable=False, blank=True)),
                ('exercse_id', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='start_date',
        ),
    ]
