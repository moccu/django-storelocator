from django.test import TestCase

from storelocator.factories import (
    ShopFactory, LocationFactory, StoreLocatorFactory)

from geopy import distance
import random


def prepare_shops(testcase):
    testcase.user_location = (52.5565, 13.3911)
    testcase.shop_locations = [
        (52.5655, 13.4001),  # 1.17 km
        (52.5745, 13.4091),  # 2.35 km
        (52.5835, 13.4181),  # 3.52 km
        (52.5925, 13.4271),  # 4.69 km
        (52.6015, 13.4361),  # 5.86 km
        (52.6105, 13.4451),  # 7.04 km
        (52.6195, 13.4541),  # 8.21 km
        (52.6285, 13.4631),  # 9.38 km
        (52.6375, 13.4721),  # 10.55 km
        (52.6465, 13.4811),  # 11.73 km
        (52.6555, 13.4901),  # 12.90 km
    ]
    random.shuffle(testcase.shop_locations)

    testcase.userpos = LocationFactory.create(
        latitude=52.5565, longitude=13.3911, postalcode='13359')

    testcase.shops = []
    testcase.storelocator = StoreLocatorFactory.create(
        name="Test Locator", slug="testlocator")
    for i, loc in enumerate(testcase.shop_locations):
        lat, lon = loc
        shop = ShopFactory.create(
            latitude=lat, longitude=lon, storelocator=testcase.storelocator)
        shop.distance = distance.distance(testcase.user_location, loc)
        testcase.shops.append(shop)


class LocationTestCase(TestCase):

    def setUp(self):
        prepare_shops(self)
