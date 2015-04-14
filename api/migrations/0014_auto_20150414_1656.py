# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0013_auto_20150408_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('complete_time', models.DateTimeField()),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'created_at', editable=False, blank=True)),
                ('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name=b'updated_at', editable=False, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BodyLocationResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body_location', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultiSelectResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0)),
                ('boolean', models.BooleanField()),
                ('number', models.IntegerField()),
                ('emotion', models.IntegerField(default=0)),
                ('percent', models.FloatField(default=0)),
                ('question_id', models.IntegerField()),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'created_at', editable=False, blank=True)),
                ('updated_at', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name=b'updated_at', editable=False, blank=True)),
                ('assessment', models.ForeignKey(to='api.Assessment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multiselectresponse',
            name='response',
            field=models.ForeignKey(related_name='multi_select', to='api.Response'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bodylocationresponse',
            name='response',
            field=models.ForeignKey(related_name='body_location', to='api.Response'),
            preserve_default=True,
        ),
    ]
