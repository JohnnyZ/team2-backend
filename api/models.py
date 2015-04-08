from django.db import models
#from djanog.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from datetime import datetime
# pip install django-enumfield
from django_enumfield import enum
from django.utils.translation import gettext as _
from django_extensions.db.fields import (CreationDateTimeField, ModificationDateTimeField,)

"""
# Puts a time stamp on all models that inherit from it 
class TimeStampedModel(models.Model):
	# comment 
	TimeStampedModel
	An abstract base class model that provides self-managed "created" and
	"modified" fields.
	# comment
	created = CreationDateTimeField(_('created'))
	modified = ModificationDateTimeField(_('modified'))

	class Meta:
		get_latest_by = 'modified'
		ordering = ('-modified', '-created',)
		abstract = True
"""

# Enum GenderType
class Gender(enum.Enum):
	# UNKNOWN
	NOT_GIVEN = 0
	MALE = 1
	FEMALE = 2

# Enum DayOfWeek
class DayOfWeek(enum.Enum):
	MO = 0
	TU = 1 
	WE = 2
	TH = 3
	FR = 4 
	SA = 5 
	SU = 6

class ResponseType(enum.Enum):
	NO = 0 
	YES = 1 
	EMOTION1 = 29

class Emotion(enum.Enum):
	NEUTRAL = 0 
	MAD = 1 
	HAPPY = 2

class BodyLocation(enum.Enum):
	HEAD = 0 

# Models here 
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	birthday = models.DateField(null=True, blank=True)
	gender = enum.EnumField(Gender, default=Gender.NOT_GIVEN)
	start_date = models.DateTimeField(default=datetime.now,blank=True)
	meditation_time = models.TimeField(null=True)
	exercise_day_of_week = enum.EnumField(DayOfWeek, default=DayOfWeek.MO)
	exercise_time = models.TimeField(null=True)
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

	def __unicode__(self):
		return self.user.get_full_name()

class MeditationSession(models.Model):
	user = models.ForeignKey(User)
	meditation_id = models.IntegerField(blank=False, null=False)
	percent_completed = models.FloatField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

class ExerciseSession(models.Model):
	user = models.ForeignKey(User)
	exercise_id = models.IntegerField(blank=False, null=False)
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

	class Meta:
		unique_together = ("user", "exercise_id")

#===========================================================================
# SIGNALS
#===========================================================================
def signals_import():
	""" 
	A note on signals.

	The signals need to be imported early on so that they get registered
	by the application. Putting the signals here makes sure of this since
	the models package gets imported on the application startup.
	"""
	from tastypie.models import create_api_key
 
	models.signals.post_save.connect(create_api_key, sender=User)
 
signals_import()

"""
class Assessment(models.Model):
	start_time = models.DateTimeField()
	complete_time = models.DateTimeField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

class Question(models.Model):
	title = models.CharField(max_length=255)
	question = models.CharField(max_length=255)

class Response(models.Model):
	user = models.ForeignKey(User)
	assessment = models.ForeignKey(Assessment)
	rtype = enum.EnumField(ResponseType, default=ResponseType.NO)
	emotion = enum.EnumField(Emotion, default=Emotion.NEUTRAL)
	percent = models.FloatField(default=0)
	question_id = models.ForeignKey(Question)
	question_answer = models.BooleanField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))
"""







