from rest_framework import serializers
from models import appUser, ExerciseSession, ExcerciseSession
from django.contrib.auth.models import User

class appUserSerializers(serializers.ModelSerializer):
	class Meta:
		model = appUser
		field = ('user')

class MeditationSerializers(serializers.ModelSerializer):
	class Meta:
		model = MeditationSession
		# Fields we want to serialize 
		field = ('meditation_id', 'user', 'percent_completed')

class ExerciseSerializers(serializers.ModelSerializer):
	class Meta:
		model = ExerciseSession
		# Fields we want to serialize 
		field = ('exercise_id', 'user', 'percent_completed')