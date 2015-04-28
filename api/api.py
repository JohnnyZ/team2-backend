from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.conf.urls import url
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from .models import *
from .exceptions import CustomBadRequest
from .constants import *
from push_notifications.api import APNSDeviceResource
from push_notifications.models import APNSDevice

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

#===========================================================================
# User Resources
#===========================================================================

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
			birthday = bundle.data["birthday"]
			# only send back date (remove time)
			bundle.data["birthday"] = birthday.date()
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
				user_profile_dict["created_at"] = user.profile.created_at
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
	apns_device = fields.ForeignKey(APNSDeviceResource, 'apns_device', null=True)
 
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

	# Serialization method that serializes the object to json before getting sent back to client
	def dehydrate(self, bundle):
		try:
			del bundle.data["apns_device"]
		except KeyError:
			pass
 
		return bundle

	# Override patch_list since it's just one (call patch_detail which calls update)
	def patch_list(self, request, **kwargs):
		kwargs["pk"] = request.user.profile.pk
		return super(UserProfileResource, self).patch_detail(request, **kwargs)

	def obj_update(self, bundle, **kwargs):
		if(bundle.request.method == "PATCH"):
			try:
				apns_token = bundle.data["apns_token"]

				apns_device = {
					'registration_id': apns_token
					}

				bundle.data["apns_device"] = apns_device
			except KeyError as missing_key:
				raise CustomBadRequest(
					code="missing_key",
					message="Must provide {missing_key} when creating a user."
							.format(missing_key=missing_key))
		else:
			kwargs["pk"] = bundle.request.user.profile.pk
		return super(UserProfileResource, self).obj_update(bundle, **kwargs)
 
	# Since there is only one user profile object, call get_detail instead
	def get_list(self, request, **kwargs):
		# Set the "pk" attribute to point at the actual User object
		kwargs["pk"] = request.user.profile.pk
		return super(UserProfileResource, self).get_detail(request, **kwargs)


#===========================================================================
# Meditaiton and Exercise Session Resources
#===========================================================================

class MeditationResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user')
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'meditation_session'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'user', 'meta']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}
		detail_uri_name = 'meditation_id'

	# This allows us to patch with the meditation_id instead of the meditation_session id
	# We don't need meditaiton_session id because meditaiton_id and user act as a composite key
	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<meditation_id>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]

	# This sets the user to be the one from the cookie
	def dispatch(self, request_type, request, **kwargs):
		kwargs['user'] = request.user#get_object_or_404(MeditationSession, username=username)
		return super(MeditationResource, self).dispatch(request_type, request, **kwargs)

	# Override update_in_place which gets called with PATCH
	# Only allow a larger percentage than the previous
	def update_in_place(self, request, original_bundle, new_data):
		old_value = original_bundle.data['percent_completed']
		new_value = float(new_data['percent_completed'])

		if(old_value < new_value):
			return super(MeditationResource, self).update_in_place(request, original_bundle, new_data)
		else:
			raise CustomBadRequest(
				code="lower_percent",
				message="precent_completed of {old_percent} is higher than the new value of {new_percent}"
						.format(old_percent=old_value, new_percent=new_value))

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


#===========================================================================
# Assessment and Response Resources
#===========================================================================

class AssessmentResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user')
	# null = true because there may be no responses on an assessment yet
	responses = fields.ToManyField('api.api.ResponseResource', "response_set", null=True, full=True)

	class Meta:
		queryset = Assessment.objects.all()
		resource_name = 'assessment'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'user', 'meta']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}

	# This sets the user to be the one from the cookie
	def dispatch(self, request_type, request, **kwargs):
		kwargs['user'] = request.user#get_object_or_404(MeditationSession, username=username)
		return super(AssessmentResource, self).dispatch(request_type, request, **kwargs)

	def override_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/get_pending_assessment%s$" %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('get_pending_assessment'), name="api_get_pending_assessment")
		]

	def get_pending_assessment(self, request, **kwargs):
		# get the last sent assessment push and if it wasn't completed, then send down id (and if it's momentary)
		# if the last sent push was completed then send down "no assessment"
		last_assessment_push = AssessmentPush.objects.filter(user__id=request.user.id).order_by("-sent")[:1]

		if(last_assessment_push.exists()):
			last_assessment_push = last_assessment_push[0]
			last_assessment_query = Assessment.objects.filter(id=last_assessment_push.assessment_id)[:1]
			last_assessment_obj = last_assessment_query[0]
			# If it exists and there is no completed time - then there is a pending assessment
			if(last_assessment_query.exists() and (last_assessment_obj.complete_time is None)):
				return self.create_response(request, model_to_dict(last_assessment_push))
		
		# raise CustomBadRequest(code="no_assessment",message="There are no pending assessments.")
		return self.create_response(request, {})


class ResponseResource(ModelResource):
	assessment = fields.ToOneField(AssessmentResource, 'assessment')
	multi_selects = fields.ToManyField('api.api.MultiSelectResponseResource', 'multi_select', related_name='response', null=True, full=True)
	body_locations = fields.ToManyField('api.api.BodyLocationResponseResource', 'body_location', related_name='response', null=True, full=True)

	class Meta:
		queryset = Response.objects.all()
		resource_name = 'response'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'meta']
		filtering = {
			'id': ALL_WITH_RELATIONS,
		}

	def obj_create(self, bundle, **kwargs):
		assessment = get_object_or_404(Assessment, pk=bundle.data['assessment_id'])
		bundle.data['assessment'] = assessment

		if assessment.user.pk != bundle.request.user.pk:
			raise CustomBadRequest(
				code="invalid_user",
				message="The user doesn't have permission to update this asssesment.")

		super(ResponseResource, self).obj_create(bundle, user=bundle.request.user)

class MultiSelectResponseResource(ModelResource):
	response = fields.ToOneField(ResponseResource, 'response')

	class Meta:
		queryset = MultiSelectResponse.objects.all()
		resource_name = 'multi_select'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'meta']
		filtering = {
			'id': ALL_WITH_RELATIONS,
		}

class BodyLocationResponseResource(ModelResource):
	response = fields.ToOneField(ResponseResource, 'response')

	class Meta:
		queryset = BodyLocationResponse.objects.all()
		resource_name = 'body_location'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['get', 'put', 'patch', 'post']
		excludes = ['resource_uri', 'meta']
		filtering = {
			'id': ALL_WITH_RELATIONS,
		}


#===========================================================================
# Pebble Notification Time Log Resource
#===========================================================================

class ExerciseReminderResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user')

	class Meta:
		queryset = ExerciseReminder.objects.all()
		resource_name = 'exercise_reminder'
		authentication = Authentication()
		authorization = Authorization()
		always_return_data = True
		allowed_methods = ['post', 'patch', 'put']
		excludes = ['resource_uri', 'meta']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}

	def obj_create(self, bundle, **kwargs):
		return super(ExerciseReminderResource, self).obj_create(bundle, user=bundle.request.user)

	# def obj_get_list(self, bundle, **kwargs):
	# 	return super(ExerciseReminderResource, self).obj_get_list(bundle, user=bundle.request.user)

