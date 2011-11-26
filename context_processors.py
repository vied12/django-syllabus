from django.contrib.sites.models import Site
from django.conf import settings
import logging

def la_base(request):
	
	site = Site.objects.get_current()
	logging.debug("'la base' loaded in context")
	return {'site': site, 'media_site' : settings.STATIC_DOC,}