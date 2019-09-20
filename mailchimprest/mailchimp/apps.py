"""
This module contains all app configurations for the mailchimp app.

------------------------------------------------------------------------

"""


import logging
from django.apps import AppConfig


logger = logging.getLogger(__name__)
del logging


class MailChimpAppConfig(AppConfig):
    name = 'mailchimp'
