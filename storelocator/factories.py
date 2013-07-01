from storelocator.models import Location, StoreLocator, Shop

import factory


class LocationFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Location

    iso = 'DE'
    postalcode = '10437'
    city = 'Berlin'
    state = 'Brandenburg'
    latitude = 52.5565
    longitude = 13.3911


class StoreLocatorFactory(factory.DjangoModelFactory):

    FACTORY_FOR = StoreLocator

    name = factory.Sequence(lambda i: 'StoreLocator-{0}'.format(i))
    slug = factory.Sequence(lambda i: 'storelocator-{0}'.format(i))


class ShopFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Shop

    type = factory.Sequence(lambda i: 'type-{0}'.format(i))
    name = factory.Sequence(lambda i: 'shop-{0}'.format(i))
    city = 'Berlin'
    postalcode = '13359'
    street = 'Drontheimerstrasse 25'
    iso = 'DE'
    storelocator = factory.SubFactory(StoreLocatorFactory)