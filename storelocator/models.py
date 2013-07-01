from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _

from geopy import distance


class Location(models.Model):

    iso = models.CharField(_('iso country code'), max_length=2)
    postalcode = models.CharField(_('postalcode'), max_length=20)
    city = models.CharField(_('place name'), max_length=180)
    state = models.CharField(_('state name'), max_length=100, blank=True)
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))
    last_updated = models.DateTimeField(_('last updated'), auto_now_add=True)

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['iso', 'postalcode']

    def __unicode__(self):
        return u'%s - %s - %s' % (self.iso, self.city, self.postalcode)


class StoreLocator(models.Model):

    CACHE_KEY = 'storelocator_%s'

    name = models.CharField(_('name'), max_length=100)
    slug = models.CharField(_('slug'), max_length=55)

    class Meta:
        verbose_name = _('store locator')
        verbose_name_plural = _('store locators')

    def __unicode__(self):
        return u'%s - <%s>' % (self.name, self.slug)


class Shop(models.Model):

    type = models.CharField(_('type'), max_length=20)
    name = models.CharField(_('name'), max_length=140)
    city = models.CharField(_('place name'), max_length=180)
    postalcode = models.CharField(_('postalcode'), max_length=20)
    street = models.CharField(_('street'), max_length=140)
    iso = models.CharField(_('iso country code'), max_length=2)
    latitude = models.FloatField(_('latitude'), blank=True, null=True)
    longitude = models.FloatField(_('longitude'), blank=True, null=True)
    storelocator = models.ForeignKey(
        StoreLocator,
        verbose_name=_('store locator'),
        related_name='shops')

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def serialize(self):
        data = model_to_dict(self, fields=(
            'name', 'city', 'postalcode', 'street', 'latitude', 'longitude'))
        data['type'] = self.type.lower()

        # distance is set in the view if lat & lon are given.
        if hasattr(self, "distance"):
            data['distance'] = round(self.distance, 2)
        else:
            data['distance'] = False
        return data

    def distance_to(self, latitude, longitude):
        location = (self.latitude, self.longitude)
        return distance.distance((latitude, longitude), location)

    def __unicode__(self):
        return u'%s - %s (%s - %s)' % (
            self.type, self.name, self.latitude, self.longitude)
