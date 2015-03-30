from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.authentication import BasicAuthentication
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from api.models import * 
from django.contrib.auth.models import User

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		authentication = BasicAuthentication()
		throttle = BaseThrottle(throttle_at=1000)
		resource_name = 'user'
		excludes = ['password', 'is_staff', 'is_superuser']
		filtering = {
			'username': ALL,
		}

class appUserResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset = appUser.objects.all()
		resource_name = 'appuser'
		filtering = {
			'user': ALL,
		}

class MeditationResource(ModelResource):
	appuser = fields.ForeignKey(appUserResource, 'appuser', full=True, blank=True)
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'meditation_session'
		filtering = {
		'appuser': ALL_WITH_RELATIONS,
		}

class ExerciseResource(ModelResource):
	class Meta:
		queryset = ExerciseSession.objects.all()
		resource_name = 'exercise_session'




