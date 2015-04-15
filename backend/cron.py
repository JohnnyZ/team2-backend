from api.models import *
from api.exceptions import CustomBadRequest
from api.constants import *

from django.shortcuts import get_object_or_404

import logging
log = logging.getLogger(__name__)

log.info("Hey there it works!!")