from django.conf.urls import patterns, include, url
from django.contrib import admin

# TastyPie
from tastypie.api import Api
from api.api import MeditationResource
v1_api = Api()
v1_api.register(MeditationResource())

meditation_resource = MeditationResource


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^backend/', include('api.urls')),
    url(r'^api/', include(v1_api.urls)),

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
)
