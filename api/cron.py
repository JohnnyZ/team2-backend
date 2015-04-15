# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404

from .models import UserProfile

import logging
logger = logging.getLogger(__name__)

def dostuff():
	records = UserProfile.objects.filter(gender=0)
	for record in records:
		print("hi")
		# logger.error(user_profile.birthday)
		# print(user_profile.headline)
		# logger.error(user_profile.headline)