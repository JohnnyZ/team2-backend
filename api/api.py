from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.conf.urls import url
from django.core import serializers
from django.forms.models import model_to_dict

from api.models import *
from api.exceptions import CustomBadRequest
from api.constants import *

from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import (
	Authentication, ApiKeyAuthentication, BasicAuthentication,
	MultiAuthentication)
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest


class CreateUserResource(ModelResource):
	user = fields.ForeignKey('api.api.UserResource', 'user', full=True)
 
	class Meta:
		allowed_methods = ['post']
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()
		queryset = UserProfile.objects.all()
		resource_name = 'create_user'
		always_return_data = True

	# Hyrdate is called during the de-serialization phase of a call
	# Deal with all the raw json here (bundle.data)
	def hydrate(self, bundle):
		# Make sure required fields are included in initial create_user api call
		REQUIRED_USER_FIELDS = ("username", "raw_password", "email", "first_name", "last_name", # User fields
								"birthday", "gender") # UserProfile fields
		for field in REQUIRED_USER_FIELDS:
			if field not in bundle.data:
				raise CustomBadRequest(
					code="missing_key",
					message="Must provide {missing_key} when creating a user."
							.format(missing_key=field))
		return bundle

	# Serialization method that serializes the object to json before getting sent back to client
	def dehydrate(self, bundle): 
		try:
			# TODO: can these be put into excludes in Meta?
			# Don't return "raw_password" in response.
			del bundle.data["raw_password"]
			# User data is already included on wrapping UserProfile data after creation
			del bundle.data["user"]
			del bundle.data["resource_uri"]
		except KeyError:
			pass
 
		return bundle

	# The method responsible for actual user creation
	def obj_create(self, bundle, **kwargs):
		try:
			# Extract the User data from request
			email = bundle.data["email"]
			username = bundle.data["username"]
			raw_password = bundle.data['raw_password']
			first_name = bundle.data["first_name"]
			last_name = bundle.data["last_name"]

			# Validate the password for length
			if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
				raise CustomBadRequest(
					code="invalid_password",
					message=(
						"Your password should contain at least {length} "
						"characters.".format(length=MINIMUM_PASSWORD_LENGTH)))

			# Separate out the User info into an object nested under the UserProfile bundle
			# This gets sorted out by the foreign key relation in UserProfileResource
			user = {
				'email': email, 
				'username': username,
				'password': make_password(raw_password),
				'first_name': first_name,
				'last_name': last_name
				}
			bundle.data['user'] = user

			# Filter for unique objects
			if User.objects.filter(email=email):
				raise CustomBadRequest(
					code="duplicate_exception",
					message="That email is already used.")
			if User.objects.filter(username=username):
				raise CustomBadRequest(
					code="duplicate_exception",
					message="That username is already used.")
		except KeyError as missing_key:
			raise CustomBadRequest(
				code="missing_key",
				message="Must provide {missing_key} when creating a user."
						.format(missing_key=missing_key))
		except User.DoesNotExist:
			pass
 
		# setting resource_name to `user_profile` here because we want
		# resource_uri in response to be same as UserProfileResource resource
		self._meta.resource_name = UserProfileResource._meta.resource_name
		bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)

		# If successfully created, log the user in and return the sessionid cookie
		username = bundle.data.get('username')
		user = authenticate(username=username, password=raw_password)
		if user:
			if user.is_active:
				login(bundle.request, user)
		return bundle

class UserResource(ModelResource):
 
	class Meta:
		authentication = Authentication()
		authorization = Authorization()
		# Because this can be updated nested under the UserProfile, it needed
		# 'put'. No idea why, since patch is supposed to be able to handle
		# partial updates.
		allowed_methods = ['get', 'patch', 'put', 'post', 'get']
		always_return_data = True
		queryset = User.objects.all()
		excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
		resource_name = 'user'
 
	#def authorized_read_list(self, object_list, bundle):
	#	return object_list.filter(id=bundle.request.user.id).select_related()

	# Serialization method that serializes the object to json before getting sent back to client
	def dehydrate(self, bundle):
		try:
			# Don't return "password" in response.
			del bundle.data["password"]
		except KeyError:
			pass
 
		return bundle

	## Since there is only one user profile object, call get_detail instead
	# def get_list(self, request, **kwargs):

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

				# Format the response json and remove unnecessary fields
				user_profile_dict = model_to_dict(user.profile)
				user_dict = model_to_dict(user)
				del user_profile_dict["user"]
				del user_dict["password"]
				del user_dict["user_permissions"]
				del user_dict["groups"]
				del user_dict["is_active"]
				del user_dict["is_staff"]
				del user_dict["is_superuser"]

				# Merge the two dictionaries
				user_response_dict = user_profile_dict.copy()
				user_response_dict.update(user_dict)
				
				return self.create_response(request,  user_response_dict)
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
 
class UserProfileResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)
 
	class Meta:
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'patch', 'put']
		detail_allowed_methods = ['get', 'patch', 'put']
		queryset = UserProfile.objects.all()
		resource_name = 'user_profile'
 
	#def authorized_read_list(self, object_list, bundle):
	#	return object_list.filter(user=bundle.request.user).select_related()

	# def obj_create(self, bundle, **kwargs):
	# 	return super(UserProfileResource, self).obj_create(bundle, user=bundle.request.user)

	def obj_update(self, bundle, request, **kwargs):
		return super(UserProfileResource, self).obj_update(bundle, request, **kwargs)
		# identity_bundle = self.build_identity_bundle(user_bundle)
		# IdentityResource().obj_update(identity_bundle, request)
		# return user_bundle
 
	# Since there is only one user profile object, call get_detail instead
	def get_list(self, request, **kwargs):
		# Set the "pk" attribute to point at the actual User object
		kwargs["pk"] = request.user.profile.pk
		return super(UserProfileResource, self).get_detail(request, **kwargs)

class MeditationResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user')
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'meditation_session'
		authentication = Authentication()
		authorization = Authorization()
		allowed_methods = ['get', 'put', 'patch', 'post']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}

class ExerciseResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user')
	class Meta:
		queryset = ExerciseSession.objects.all()
		resource_name = 'exercise_session'
		authentication = Authentication()
		authorization = Authorization()
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'user', 'meta']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}

	# Serialization method that serializes the object to json before getting sent back to client
	def dehydrate(self, bundle):
		try:
			# Remove unneeded fields
			del bundle.data["resource_uri"]
			del bundle.data["user"]
		except KeyError:
			pass
 
		return bundle

	def obj_create(self, bundle, **kwargs):
		return super(ExerciseResource, self).obj_create(bundle, user=bundle.request.user)

	def obj_get_list(self, bundle, **kwargs):
		return super(ExerciseResource, self).obj_get_list(bundle, user=bundle.request.user)




