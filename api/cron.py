from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404

from .api import *

import logging
logger = logging.getLogger(__name__)

def dostuff():
	for user_profile in UserProfile.objects.all():
		print("hi")
		# logger.error(user_profile.birthday)
		# print(user_profile.headline)
		# logger.error(user_profile.headline)