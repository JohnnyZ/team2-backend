from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.conf.urls import url
from api.models import *

from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest

class appUserResource(ModelResource):
	class Meta:
		queryset = appUser.objects.all()
		resource_name = 'appuser'
		authorization = Authorization()

class UserResource(ModelResource):
	appuser = fields.ToOneField(appUserResource, attribute='appuser', related_name='user', full=True, null=True)
	class Meta:
		queryset = User.objects.all()
		authentication = BasicAuthentication()
		throttle = BaseThrottle(throttle_at=1000)
		resource_name = 'user'
		allowed_methods = ['get', 'post']
		excludes = ['password', 'is_staff', 'is_superuser', 'is_active']
		filtering = {
			'username': ALL,
		}

	def override_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/login%s$" %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('login'), name="api_login"),
			url(r'^(?P<resource_name>%s)/logout%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('logout'), name='api_logout'),
		]

	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])

		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

		username = data.get('username', '')
		password = data.get('password', '')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return self.create_response(request, {
					'success': True
				})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
					}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )

	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		if request.user and request.user.is_authenticated():
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)

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




