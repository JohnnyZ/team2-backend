from django.db import models
#from djanog.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
# pip install django-enumfield
from django_enumfield import enum
from django.utils.translation import gettext as _

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
class GenderType(enum.Enum):
	# UNKNOWN
	UNKNOWN = 0
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
class appUser(models.Model):
	#first_name = models.CharField(max_length=150)
	#last_name = models.CharField(max_length=150)
	#email = models.EmailField('email address', unique=True)
	user = models.ForeignKey(User)
	password = models.CharField(_('password'), max_length=128)
	birthday = models.DateField(null=True, blank=True)
	gender = enum.EnumField(GenderType, default=Gender.UNKNOWN)
	start_date = models.DateTimeField(default=datetime.now,blank=True)
	mediation_time = models.DateTimeField()
	excercise_day_of_week = enum.EnumField(DayOfWeek, default=DayOfWeek.MO)
	excercise_time = models.DateTimeField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))
class MeditationSession(models.Model):
	meditation_id = models.IntegerField()
	user = models.ForeignKey(User)
	percent_completed = models.FloatField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))
class ExcerciseSession(models.Model):
	Excercise_id = models.IntegerField()
	user = models.ForeignKey(User)
	percent_completed = models.FloatField()
	created_at = CreationDateTimeField(_('created_at'))
	updated_at = ModificationDateTimeField(_('updated_at'))

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







