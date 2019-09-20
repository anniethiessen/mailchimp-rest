"""
This file contains all WSGI configurations.

It exposes the WSGI callable as a module-level variable named
application.

------------------------------------------------------------------------

"""


import os
import logging

from django.core.wsgi import get_wsgi_application


logger = logging.getLogger(__name__)
del logging


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'mailchimprest.settings.local'
)

application = get_wsgi_application()
