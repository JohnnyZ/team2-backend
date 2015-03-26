from django.shortcuts import render
from rest_framework import generics 
from serializers import MeditationSerializers
from models import MeditationSession

class MeditationSessionList(generics.ListCreateAPIView):
	queryset = MeditationSession.objects.all()
	serializer_class = ZipSerializer

# All update delete handling
class MeditationSessionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = MeditationSession.objects.all()
	serializer_class = ZipSerializer