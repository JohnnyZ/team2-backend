# from django.shortcuts import get_object_or_404

import logging
logger = logging.getLogger(__name__)
 
def myfunction():
    logger.debug("this is a debug message!")
 
def myotherfunction():
    logger.error("this is an error message!!")