from django.conf.urls import patterns, url

from .views import StoreLocatorView


urlpatterns = patterns('storelocator.urls',
    url(r"^(?P<slug>[\w-]+)\.json$", StoreLocatorView.as_view(), name="storelocator"),
)