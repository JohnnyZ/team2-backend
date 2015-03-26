from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from api.models import * 
from django.contrib.auth.models import User

class MeditationResource(ModelResource):
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'meditation_session'

class ExerciseResource(ModelResource):
	class Meta:
		queryset = ExerciseSession.objects.all()
		resource_name = 'exercise_session'

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_staff', 'is_superuser']

class appUserResource(ModelResource):
	class Meta:
		queryset = appUser.objects.all()
		resource_name = 'appuser'


