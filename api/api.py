from django.contrib.auth.models import User
from django.db import IntegrityError
from api.models import *

from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest


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

class UserSignUpResource(ModelResource):
    class Meta:
        object_class = User
        resource_name = 'signup'
        fields = ['username', 'first_name', 'last_name', 'email']
        allowed_methods = ['post']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        queryset = User.objects.all()

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(UserSignUpResource, self).obj_create(bundle)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('Username already exists')

        return bundle

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




