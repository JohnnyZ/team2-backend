from django.conf.urls import patterns, include, url
from django.contrib import admin

# TastyPie
from tastypie.api import Api
from api.api import *

v1_api = Api(api_name='v1')
v1_api.register(MeditationResource())
v1_api.register(ExerciseResource())
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(CreateUserResource())

v1_api.register(AssessmentResource())
v1_api.register(ResponseResource())
v1_api.register(MultiSelectResponseResource())
v1_api.register(BodyLocationResponseResource())
v1_api.register(ExerciseReminderResource())

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'backend.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	#url(r'^backend/', include('api.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),

	#url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
)
