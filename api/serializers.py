from rest_framework import serializers
from api.models import appUser, ExerciseSession, MeditationSession
from django.contrib.auth.models import User

# Need to make edits to this 
"""
class appUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = appUser
		field = ('user')
"""

class MeditationSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeditationSession
		# Fields we want to serialize 
		field = ('meditation_id', 'user', 'percent_completed')

class ExerciseSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExerciseSession
		# Fields we want to serialize 
		field = ('exercise_id', 'user', 'percent_completed')