from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.conf.urls import url
from .models import UserProfile
from .utils import MINIMUM_PASSWORD_LENGTH, validate_password
from .exceptions import CustomBadRequest

from django.core import serializers


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
 
    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ("birthday", "user")
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
 
        REQUIRED_USER_FIELDS = ("username", "email", "first_name", "last_name",
                                "raw_password")
        for field in REQUIRED_USER_FIELDS:
            if field not in bundle.data["user"]:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
        return bundle
 
    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data["user"]["email"]
            username = bundle.data["user"]["username"]
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
        return super(CreateUserResource, self).obj_create(bundle, **kwargs)

class UserResource(ModelResource):
    # We need to store raw password in a virtual field because hydrate method
    # is called multiple times depending on if it's a POST/PUT/PATCH request
    raw_password = fields.CharField(attribute=None, readonly=True, null=True,
                                    blank=True)
 
    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = Authentication()
        authorization = Authorization()
 
        # Because this can be updated nested under the UserProfile, it needed
        # 'put'. No idea why, since patch is supposed to be able to handle
        # partial updates.
        allowed_methods = ['get', 'patch', 'put', ]
        always_return_data = True
        queryset = User.objects.all()#.select_related("api_key")
        excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login']
 
    #def authorized_read_list(self, object_list, bundle):
    #    return object_list.filter(id=bundle.request.user.id).select_related()
 
    def hydrate(self, bundle):
        if "raw_password" in bundle.data:
            # Pop out raw_password and validate it
            # This will prevent re-validation because hydrate is called
            # multiple times
            # https://github.com/toastdriven/django-tastypie/issues/603
            # "Cannot resolve keyword 'raw_password' into field." won't occur
 
            raw_password = bundle.data.pop["raw_password"]
 
            # Validate password
            if not validate_password(raw_password):
                if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
                    raise CustomBadRequest(
                        code="invalid_password",
                        message=(
                            "Your password should contain at least {length} "
                            "characters.".format(length=
                                                 MINIMUM_PASSWORD_LENGTH)))
                raise CustomBadRequest(
                    code="invalid_password",
                    message=("Your password should contain at least one number"
                             ", one uppercase letter, one special character,"
                             " and no spaces."))
 
            bundle.data["password"] = make_password(raw_password)
 
        return bundle
 
    def dehydrate(self, bundle):
        #bundle.data['key'] = bundle.obj.api_key.key
 
        try:
            # Don't return `raw_password` in response.
            del bundle.data["raw_password"]
        except KeyError:
            pass
 
        return bundle
 
 
class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
 
    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'
 
    #def authorized_read_list(self, object_list, bundle):
    #    return object_list.filter(user=bundle.request.user).select_related()
 
    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(UserProfileResource, self).get_detail(request, **kwargs)
"""
class CreateUserResource(ModelResource):
	appuser = fields.ToOneField(UserProfileResource, 'appuser', related_name='user', full=True)
	class Meta:
		object_class = User
		resource_name = 'signup'
		fields = ['username', 'first_name', 'last_name', 'email']
		allowed_methods = ['post']
		always_return_data = True 
		include_resource_uri = False
		authentication = Authentication()
		authorization = Authorization()
		queryset = User.objects.all()

	def obj_create(self, bundle, request=None, **kwargs):
		try:
			bundle = super(CreateUserResource, self).obj_create(bundle)
			password = bundle.data.get('password')
			username = bundle.data.get('username')
			bundle.obj.set_password(bundle.data.get('password'))
			bundle.obj.save()
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(bundle.request, user)
		except IntegrityError:
			raise BadRequest('Username already exists')

		return bundle

class UserProfileResource(ModelResource):
	user = fields.ToOneField('api.api.UserResource', attribute='user', related_name='appuser')
	birthday = fields.DateField(null=True, blank=True, attribute='birthday')
	class Meta:
		queryset = UserProfile.objects.all()
		resource_name = 'appuser'
		authorization = Authorization()

class UserResource(ModelResource):
	appuser = fields.ToManyField(UserProfileResource, 'appuser', related_name='user', full=True, null=True)
	class Meta:
		queryset = User.objects.all()
		authentication = Authentication()
		authorization = Authorization()
		throttle = BaseThrottle(throttle_at=1000)
		resource_name = 'user'
		allowed_methods = ['get', 'post']
		excludes = ['password', 'is_staff', 'is_superuser', 'is_active']
		filtering = {
			'username': ALL,
			'id': ALL,
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
				user_json = serializers.serialize('json', [ user, ])
				return self.create_response(request, {
					'success': True,
					'user': user_json
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
"""

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
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}

	def obj_create(self, bundle, **kwargs):
		return super(ExerciseResource, self).obj_create(bundle, user=bundle.request.user)

	def obj_get_list(self, bundle, **kwargs):
		return super(ExerciseResource, self).obj_get_list(bundle, user=bundle.request.user)




