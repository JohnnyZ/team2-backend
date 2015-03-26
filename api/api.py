from tastypie.resources import ModelResource
from api.models import * 

class MeditationResource(ModelResource):
	class Meta:
		queryset = MeditationSession.objects.all()
		resource_name = 'medsession'
