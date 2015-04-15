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
	MALE = 0
	FEMALE = 1

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
	BOOLEAN = 0
	NUMBER = 1
	EMOTION = 2
	PERCENT = 3
	MULTI_SELECT = 4
	BODY_MAP = 5

class Emotion(enum.Enum):
	NONE = 0 
	UPSET = 1 
	SAD = 2 
	DEPRESSED = 3
	NERVOUS = 4
	ANXIOUS = 5
	HAPPY = 6
	CONTENT = 7
	EXCITED = 8
	ENERGETIC = 9
	RELAXED = 10
	ALERT = 11

class BodyLocation(enum.Enum):
	NONE = 0 
	HEAD = 1
	THROAT = 2
	CHEST = 3
	STOMACH = 4
	ARMS = 5
	HANDS = 6
	FACE = 7
	SHOULDERS = 8
	UPPER_BACK = 9
	LOWER_BACK = 10
	THIGHS = 11
	KNEE = 12
	FEET = 13

# Models here 
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	birthday = models.DateField(null=True, blank=True)
	gender = enum.EnumField(Gender, default=Gender.MALE)
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
	meditation_id = models.IntegerField(blank=False, null=False) # foreign key to local meditation_id
	percent_completed = models.FloatField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

class ExerciseSession(models.Model):
	user = models.ForeignKey(User)
	exercise_id = models.IntegerField(blank=False, null=False) # foreign key to local exercise_idb
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

	class Meta:
		unique_together = ("user", "exercise_id")


### Assessments

class Assessment(models.Model):
	user = models.ForeignKey(User)
	start_time = models.DateTimeField(null=True, blank=True)
	complete_time = models.DateTimeField(null=True, blank=True)
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

class Response(models.Model):
	assessment = models.ForeignKey(Assessment)
	type = enum.EnumField(ResponseType)
	boolean = models.BooleanField(default=True)
	number = models.IntegerField(null=True, blank=True)
	emotion = enum.EnumField(Emotion, default=Emotion.NONE)
	percent = models.FloatField(default=0)
	question_id = models.IntegerField(blank=False, null=False) # foreign key to local question_id
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

	def __unicode__(self):
		return self.question_id()

class MultiSelectResponse(models.Model):
	response = models.ForeignKey(Response, related_name="multi_select")
	selection_id = models.IntegerField(blank=False, null=False) # foreign key to local selection_id

class BodyLocationResponse(models.Model):
	response = models.ForeignKey(Response, related_name="body_location")
	body_location = enum.EnumField(BodyLocation, default=BodyLocation.NONE)



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


