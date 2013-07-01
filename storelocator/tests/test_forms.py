from django.test import TestCase

from storelocator.forms import StoreLocatorForm


class StoreLocatorFormTest(TestCase):

    def test_form_empty_invalid(self):
        form = StoreLocatorForm({})
        valid = form.is_valid()
        self.assertEqual(1, len(form.errors))
        self.assertTrue(form.non_field_errors())
        self.assertFalse(valid)

    def test_form_valid_latlon(self):
        form = StoreLocatorForm({'latitude': 48.0, 'longitude': 6.0})
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_form_valid_postalcode(self):
        form = StoreLocatorForm({'postalcode': '13359', 'iso': 'DE'})
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_form_invalid_postalcode(self):
        form = StoreLocatorForm({'postalcode': '13359'})
        valid = form.is_valid()
        self.assertFalse(valid)

    def test_limit_validator_valid(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'limit': 1
        })
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_limit_validator_invalid_min(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'limit': -1
        })
        valid = form.is_valid()
        self.assertFalse(valid)
        self.assertIn('limit', form.errors)

    def test_limit_validator_invalid_max(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'limit': 16
        })
        valid = form.is_valid()
        self.assertFalse(valid)
        self.assertIn('limit', form.errors)

    def test_radius_validator_valid(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'radius': 8.0
        })
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_radius_validator_invalid_min(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'radius': -1
        })
        valid = form.is_valid()
        self.assertFalse(valid)
        self.assertIn('radius', form.errors)

    def test_radius_validator_invalid_max(self):
        form = StoreLocatorForm({
            'postalcode': '13359',
            'iso': 'DE',
            'radius': 11.0
        })
        valid = form.is_valid()
        self.assertFalse(valid)
        self.assertIn('radius', form.errors)
