from django.test import TestCase

from storelocator.importers import locations, shops
from storelocator.factories import StoreLocatorFactory
from storelocator.models import Location, Shop

import os


class LocationImportTest(TestCase):

    def setUp(self):
        self.csv = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'testdata', 'testlocations.csv'))
        self.importer = locations.GeonamesLocationImporter(
            self.csv, dialect='excel-tab')

    def test_import_locations(self):
        self.importer.run()
        locations = Location.objects.all()
        self.assertEqual(3, locations.count())
        self.assertEqual(2, Location.objects.filter(iso='DE').count())
        self.assertEqual(1, Location.objects.filter(iso='RU').count())


class ShopImportTest(TestCase):

    def setUp(self):
        self.storelocator = StoreLocatorFactory.create()
        self.csv = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'testdata', 'testshops.csv'))
        self.importer = shops.ShopImporter(
            self.csv, dialect='excel-tab', delimiter=',')

    def test_import_locations(self):
        self.importer.run(self.storelocator.id)
        shops = Shop.objects.all()
        self.assertEqual(4, shops.count())
