"""
This module will contain all mailchimp for the task app.

------------------------------------------------------------------------

"""


import logging
import hashlib

from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from django.conf import settings

from .serializers import (
    MailChimpEmailHashSerializer,
    MailChimpMemberSerializer
)


logger = logging.getLogger(__name__)
del logging
client = settings.MAILCHIMP_CLIENT


class MailChimpRootView(GenericAPIView):
    """
    get:
    Return MailChimp links.

    > **Member List/Create**<br/>
    >> `../members/`<br/>
    >> ### GET: Allows clients to list all MailChimp members
    >> ### POST: Allows clients to create a new MailChimp member
    <br/>

    > **Member Retrieve/Update/Delete**<br/>
    >> `../members/<pk>/`<br/>
    >> ### GET: Allows clients to retrieve a MailChimp member
    >> ### PUT: Allows clients to update a MailChimp member
    >> ### DESTROY: Allows clients to delete a MailChimp member
    <br/>

    > **Member Tag List/Create**<br/>
    >> `../members/<pk>/tags/`<br/>
    >> ### GET: Allows clients to list all a MailChimp member's tags
    >> ### POST: Allows clients to create a new MailChimp member's tag
    <br/>

    > **Member Tag Retrieve/Update/Delete**<br/>
    >> `../members/<pk>/tags/<pk>/`<br/>
    >> ### GET: Allows clients to retrieve a MailChimp member's tag
    >> ### PUT: Allows clients to update a MailChimp member's tag
    >> ### DESTROY: Allows clients to delete a MailChimp member's tag
    <br/>

    """

    def get(self, request):
        data = {
            '_members': reverse(
                viewname='mailchimp-urls:member-list-create',
                request=request
            )
        }
        return Response(data, status=HTTP_200_OK)


class MailChimpEmailHashRetrieveView(RetrieveAPIView):
    """
    get:
    Return MD5 hash encoded email.

    `email` must be included in query parameters

    """

    # TO DO permissions
    serializer_class = MailChimpEmailHashSerializer

    def get_object(self):
        if 'email' not in self.request.query_params:
            return {}

        email = self.request.query_params['email'].lower()
        md5_hash = hashlib.md5(email.encode('utf-8'))

        return {
            "email": email,
            "hash": md5_hash.hexdigest()
        }


class MailChimpMemberListCreateView(ListCreateAPIView):
    """
    get:
    Return MailChimp members list.

    post:
    Create new MailChimp member.

    """

    # TO DO paginate
    # TO DO permissions
    serializer_class = MailChimpMemberSerializer

    def get_queryset(self):
        return client.lists.members.all(
            list_id=settings.MAILCHIMP_LIST_ID,
            get_all=True,
            fields=','.join(
                [f'members.{f}' for f in settings.MAILCHIMP_MEMBER_FIELDS])
        )['members']


class MailChimpMemberRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Return MailChimp member.

    put:
    Update MailChimp member.

    patch:
    Partial update MailChimp member.

    destroy:
    Delete MailChimp member.

    """

    # TO DO permissions
    serializer_class = MailChimpMemberSerializer

    def get_object(self):
        return client.lists.members.get(
            list_id=settings.MAILCHIMP_LIST_ID,
            subscriber_hash=self.kwargs['member_id'],
            fields=','.join([f for f in settings.MAILCHIMP_MEMBER_FIELDS])
        )

    def perform_destroy(self, instance):
        return client.lists.members.delete(
            list_id=settings.MAILCHIMP_LIST_ID,
            subscriber_hash=self.kwargs['member_id']
        )
