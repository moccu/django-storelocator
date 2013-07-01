from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Location, StoreLocator, Shop


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'postalcode', 'iso', 'city', 'state', 'latitude', 'longitude',
        'last_updated'
    )

    ordering = ['postalcode',]

    list_filter = [
        'iso',
    ]

    search_fields = ('state', 'city', 'iso', 'postalcode')


class StoreLocatorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )

    search_fields = ('name', 'slug')


class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'street', 'postalcode', 'city',
        'iso', 'latitude', 'longitude', 'get_storelocator_name'
    )
    search_fields = ('name', 'city', 'postalcode', 'street')
    list_filter = ('type', 'storelocator__name')
    raw_id_fields = ('storelocator', )

    def get_storelocator_name(self, obj):
        url = reverse('admin:%s_%s_change' % (
            obj.storelocator._meta.app_label,
            obj.storelocator._meta.module_name
        ), args=[obj.storelocator.id] )
        return u'<a href="%s">%s</a>' % (url,  obj.storelocator.name)
    get_storelocator_name.short_description = 'storelocator'
    get_storelocator_name.allow_tags = True


admin.site.register(Location, LocationAdmin)
admin.site.register(StoreLocator, StoreLocatorAdmin)
admin.site.register(Shop, ShopAdmin)