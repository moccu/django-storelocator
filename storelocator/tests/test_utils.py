from .testcase import LocationTestCase
from storelocator.factories import StoreLocatorFactory
from storelocator.utils import get_near_shops


class GetNearShopsTest(LocationTestCase):

    def test_get_near_shops(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            5,
            10.0,
            True)

        self.assertEqual(5, len(shops))
        for shop in shops:
            self.assertTrue(shop.distance <= 5.9)  # 5th shop has dist 5.86

    def test_smaller_range(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            5,
            5,
            True)

        self.assertEqual(4, len(shops))
        for shop in shops:
            self.assertTrue(shop.distance <= 4.7)  # 4th shop has dist 4.69

    def test_range(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            15,
            13.0,
            True)

        self.assertEqual(11, len(shops))
        for shop in shops:
            self.assertTrue(shop.distance <= 13.0)  # last shop has dist 12.90

    def test_other_storelocator(self):
        storelocator2 = StoreLocatorFactory.create(
            name="Store Locator 2", slug="store-locator-2")

        shops = get_near_shops(
            storelocator2,
            self.userpos.latitude,
            self.userpos.longitude,
            15,
            10.0,
            True)

        self.assertEqual(0, len(shops))

    def test_iso_filtering(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            15,
            10.0,
            True,
            'NL')
        self.assertEqual(0, len(shops))

    def test_no_distance_property(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            5,
            1.17,
            False)

        self.assertEqual(1, len(shops))
        self.assertFalse(hasattr(shops[0], "distance"))

    def test_distance_filter(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            5,
            2.35,
            True)

        self.assertEqual(2, len(shops))

    def test_limit_one(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            1,
            10.0,
            True)

        self.assertEqual(1, len(shops))

    def test_limit_zero(self):
        shops = get_near_shops(
            self.storelocator,
            self.userpos.latitude,
            self.userpos.longitude,
            0,
            10.0,
            True)

        self.assertEqual(0, len(shops))
