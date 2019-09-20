"""
This module will contain all serializers for the mailchimp app.

------------------------------------------------------------------------

"""


import logging
import itertools

from rest_framework.serializers import (
    Serializer,
    BooleanField,
    CharField,
    ChoiceField,
    DateTimeField,
    EmailField,
    SerializerMethodField
)

from django.conf import settings

from .relations import DictHyperlinkedIdentityField


logger = logging.getLogger(__name__)
del logging
client = settings.MAILCHIMP_CLIENT


class MailChimpEmailHashSerializer(Serializer):
    email = EmailField(read_only=True)
    hash = CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MailChimpMemberSerializer(Serializer):
    FREE_ACCESS = 'Free'
    DONOR_ACCESS = 'Donor'
    GRANTED_ACCESS = 'Granted'

    ACCESS_TIER_CHOICES = [
        FREE_ACCESS,
        DONOR_ACCESS,
        GRANTED_ACCESS
    ]

    TAG_GROUPS = {
        'is_staff': [False, True],
        'is_active': [False, True],
        'is_verified': [False, True],
        'is_linked': [False, True],
        'access_tier': ACCESS_TIER_CHOICES
    }

    _self = DictHyperlinkedIdentityField(
        view_name='mailchimp-urls:member-retrieve-update-destroy',
        lookup_field='id',
        lookup_url_kwarg='member_id'
    )
    id = CharField(
        read_only=True
    )
    email_address = EmailField()
    first_name = CharField(
        allow_blank=True,
        default='',
        required=False,
        source='merge_fields.FNAME'
    )
    last_name = CharField(
        allow_blank=True,
        default='',
        required=False,
        source='merge_fields.LNAME'
    )
    status = CharField(
        read_only=True
    )
    created_on = DateTimeField(
        source='timestamp_signup'
    )
    last_changed = DateTimeField(
        read_only=True
    )
    tags = SerializerMethodField()
    is_staff = BooleanField(
        default=False,
        required=False,
        write_only=True
    )
    is_active = BooleanField(
        default=False,
        required=False,
        write_only=True
    )
    is_verified = BooleanField(
        default=False,
        required=False,
        write_only=True
    )
    is_linked = BooleanField(
        default=False,
        required=False,
        write_only=True
    )
    access_tier = ChoiceField(
        choices=ACCESS_TIER_CHOICES,
        default=FREE_ACCESS,
        required=False,
        write_only=True
    )

    def get_tags(self, obj):
        return sorted([tag['name'] for tag in obj['tags']])

    def generate_tag_data(self, group, value):
        tag_list = []
        for choice in self.TAG_GROUPS[group]:
            status = 'active' if value == choice else 'inactive'
            tag_list.append(
                {
                    "name": f'{group}: {choice}',
                    "status": status
                }
            )
        return tag_list

    def validate_created_on(self, value):
        return value.isoformat()

    def validate_is_staff(self, value):
        return self.generate_tag_data('is_staff', value)

    def validate_is_active(self, value):
        return self.generate_tag_data('is_active', value)

    def validate_is_verified(self, value):
        return self.generate_tag_data('is_verified', value)

    def validate_is_linked(self, value):
        return self.generate_tag_data('is_linked', value)

    def validate_access_tier(self, value):
        return self.generate_tag_data('access_tier', value)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['status'] = 'subscribed'
        attrs['tags'] = list(
            itertools.chain.from_iterable(
                attrs.pop(tag) for tag in self.TAG_GROUPS.keys() if
                tag in attrs
            )
        )
        return attrs

    def create(self, validated_data):
        tag_data = validated_data.pop('tags', None)

        response = client.lists.members.create(
            list_id=settings.MAILCHIMP_LIST_ID,
            data=validated_data
        )

        if tag_data:
            client.lists.members.tags.update(
                list_id=settings.MAILCHIMP_LIST_ID,
                subscriber_hash=response['id'],
                data={'tags': tag_data}
            )

        return client.lists.members.get(
            list_id=settings.MAILCHIMP_LIST_ID,
            subscriber_hash=response['id'],
            fields=','.join([f for f in settings.MAILCHIMP_MEMBER_FIELDS])
        )

    def update(self, instance, validated_data):
        tag_data = validated_data.pop('tags', None)

        response = client.lists.members.update(
            list_id=settings.MAILCHIMP_LIST_ID,
            subscriber_hash=instance['id'],
            data=validated_data
        )

        if tag_data:
            client.lists.members.tags.update(
                list_id=settings.MAILCHIMP_LIST_ID,
                subscriber_hash=response['id'],
                data={'tags': tag_data}
            )

        return client.lists.members.get(
            list_id=settings.MAILCHIMP_LIST_ID,
            subscriber_hash=response['id'],
            fields=','.join([f for f in settings.MAILCHIMP_MEMBER_FIELDS])
        )
