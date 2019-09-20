"""
This module contains all mailchimp url configurations.

------------------------------------------------------------------------

"""


import logging

from django.urls import path

from .views import (
    MailChimpEmailHashRetrieveView,
    MailChimpMemberListCreateView,
    MailChimpMemberRetrieveUpdateDestroyView,
    MailChimpRootView,
)


logger = logging.getLogger(__name__)
del logging
app_name = 'mailchimp'


# TO DO favicon
# TO DO debugger
urlpatterns = [
    path(
        '',
        MailChimpRootView.as_view(),
        name='root'
    ),
    path(
        'email-hash/',
        MailChimpEmailHashRetrieveView.as_view(),
        name='email-hash-retrieve'
    ),
    path(
        'members/',
        MailChimpMemberListCreateView.as_view(),
        name='member-list-create'
    ),
    path(
        'members/<member_id>/',
        MailChimpMemberRetrieveUpdateDestroyView.as_view(),
        name='member-retrieve-update-destroy'
    )
]