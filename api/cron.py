from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import *

import logging
logger = logging.getLogger(__name__)

def dostuff():
	for user_profile in UserProfile.objects.all():
		logger.error(user_profile.user.email)
		print(user_profile.user.email)