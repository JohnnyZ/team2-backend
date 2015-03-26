from django.shortcuts import render
from rest_framework import generics 
from api.serializers import MeditationSerializer
from api.models import MeditationSession

class MeditationSessionList(generics.ListCreateAPIView):
	queryset = MeditationSession.objects.all()
	serializer_class = MeditationSerializer

# All update delete handling
class MeditationSessionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = MeditationSession.objects.all()
	serializer_class = MeditationSerializer