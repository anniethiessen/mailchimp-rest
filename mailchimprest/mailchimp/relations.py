"""
This module will contain custom relation classes for the mailchimp app.

------------------------------------------------------------------------

"""


from rest_framework.relations import HyperlinkedIdentityField


class DictHyperlinkedIdentityField(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = obj[self.lookup_field]
        kwargs = {self.lookup_url_kwarg: lookup_value}
        return self.reverse(
            view_name,
            kwargs=kwargs,
            request=request,
            format=format
        )
