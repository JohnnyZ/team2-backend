from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from api.models import * 
from django.contrib.auth.models import User

class MeditationResource(ModelResource):
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'medsession'

class SessionResource(ModelResource):
	class Meta:
		queryset = SessionResource.objects.all()
		resource_name = 'medsession'

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'

class appUserResource(ModelResource):
	class Meta:
		queryset = appUser.objects.all()
		resource_name = 'appuser'


