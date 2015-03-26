from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from api.models import * 


class MeditationResource(ModelResource):
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'medsession'
