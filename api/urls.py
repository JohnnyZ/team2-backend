from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views 

urlpatterns = patterns('', 
		#url(r'^api/$', views.MeditationSessionList.as_view()),
		url(r'^api22/(?P<pk>[0-9]+)/$', views.MeditationSessionDetail.as_view()),
		)

#urlpatters = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])