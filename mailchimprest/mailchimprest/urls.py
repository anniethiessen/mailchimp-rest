"""
This module contains all url configurations.

------------------------------------------------------------------------

"""


import logging
from django.urls import path, include


logger = logging.getLogger(__name__)
del logging


# TO DO favicon
# TO DO debugger
# TO DO docs
# TO DO browsable pages
urlpatterns = [
    path(
        'auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework-urls'
        )
    ),
    path(
        'mailchimp/',
        include(
            'mailchimp.urls',
            namespace='mailchimp-urls'
        )
    )
]
