from django import forms
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class StoreLocatorForm(forms.Form):

    limit_max = getattr(settings, 'STORELOCATOR_LIMIT_MAX', 15)
    radius_max = getattr(settings, 'STORELOCATOR_RADIUS_MAX', 10.0)

    postalcode = forms.CharField(max_length=20, required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    iso = forms.CharField(max_length=2, required=False)
    limit = forms.IntegerField(required=False, validators=[
        MinValueValidator(0), MaxValueValidator(limit_max)])
    radius = forms.FloatField(required=False, validators=[
        MinValueValidator(0.1), MaxValueValidator(radius_max)])

    def clean(self):
        cleaned_data = super(StoreLocatorForm, self).clean()

        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        postalcode = cleaned_data.get('postalcode')
        iso = cleaned_data.get('iso')

        # check if all fields are empty
        if not latitude and not longitude and not postalcode:
            if (not 'latitude' in self._errors and
                not 'longitude' in self._errors and
                not 'postalcode' in self._errors):
                raise forms.ValidationError(
                    _("'postalcode' or 'latitude' and "
                      "'longitude' are required."))

        if latitude and longitude:
            return cleaned_data

        if postalcode:
            if not iso:
                raise forms.ValidationError(
                    _("'iso' is required."))

        return cleaned_data
