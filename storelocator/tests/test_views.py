from django.core.cache import cache
from django.core.urlresolvers import reverse

from .testcase import LocationTestCase

import json
import urllib


class LocationFormViewTest(LocationTestCase):

    def test_404_response(self):
        response = self.client.get(
            reverse('storelocator', args=['invalid']))
        self.assertEqual(404, response.status_code)

    def test_405_response(self):
        response = self.client.post(
            reverse('storelocator', args=['testlocator']))
        self.assertEqual(405, response.status_code)

    def test_nearby_shops_postalcode(self):
        form_data = {'postalcode': '13359', 'iso': 'DE'}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(True, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertTrue(json_response['shops'])
        self.assertFalse(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_no_nearby_shops_postalcode(self):
        form_data = {'postalcode': '12345', 'iso': 'DE'}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(True, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(json_response['shops']))
        self.assertFalse(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_postalcode_no_iso(self):
        form_data = {'postalcode': '12345'}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(False, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(json_response['shops']))
        self.assertTrue(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_nearby_shops_latlon(self):
        form_data = {'latitude': 52.5565, 'longitude': 13.3911}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(True, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertTrue(json_response['shops'])
        self.assertFalse(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_no_nearby_shops_latlon(self):
        form_data = {'latitude': 53.5565, 'longitude': 14.3911}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(True, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(json_response['shops']))
        self.assertFalse(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_empty_querystring(self):
        form_data = {}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertTrue(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_jsonp_response(self):
        form_data = {'callback': 'jsonp'}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        self.assertIn("jsonp", response.content)

    def test_position_postalcode(self):
        """
        If both latlon and postalcode are passed as parameters, then latlon
        should have priority.
        """
        form_data = {
            'latitude': 52.5565, 'longitude': 13.3911, 'postalcode': 13359
        }
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertEqual(True, json_response['success'])
        self.assertEqual(200, response.status_code)
        self.assertTrue(json_response['shops'])
        self.assertFalse(json_response['non_field_errors'])
        self.assertFalse(json_response['form_errors'])

    def test_postalcode_distance(self):
        form_data = {'postalcode': '13359', 'iso': 'DE'}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertFalse(json_response['shops'][0]['distance'])

    def test_latlon_distance(self):
        form_data = {'latitude': 52.5565, 'longitude': 13.3911}
        encoded = urllib.urlencode(form_data)
        response = self.client.get(
            reverse('storelocator', args=['testlocator'])+'?'+encoded)
        json_response = json.loads(response.content)
        self.assertTrue(json_response['shops'][0]['distance'])

    def test_num_queries(self):
        cache.clear()
        form_data = {'postalcode': '13359', 'iso': 'DE'}
        encoded = urllib.urlencode(form_data)

        with self.assertNumQueries(3):
            self.client.get(
                reverse('storelocator', args=['testlocator'])+'?'+encoded)

        with self.assertNumQueries(0):
            self.client.get(
                reverse('storelocator', args=['testlocator'])+'?'+encoded)
