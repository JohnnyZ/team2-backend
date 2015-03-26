from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin

from api.api import MeditationResource

meditation_resource = MeditationResource


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include('api.urls')),
    url(r'^api/', include(meditation_resource.urls)),

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
)
