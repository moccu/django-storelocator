from .models import Shop

import logging
import requests
import time


logger = logging.getLogger('storelocator')


def update_shops():
    limit = 2500
    for shop in Shop.objects.filter(latitude=None, longitude=None)[:limit]:
        location = "%s %s %s" % (shop.city, shop.postalcode, shop.street)
        try:
            json = reverse_geocoding(location)
        except requests.HTTPError:
            continue

        geo = json['results'][0]['geometry']['location']
        shop.latitude = geo['lat']
        shop.longitude = geo['lng']
        shop.save()
        logger.debug('Saved lat & lon for: %s' % shop)


def reverse_geocoding(location):
    url = "http://maps.googleapis.com/maps/api/geocode/json"
    qs = "?address=%s&components=country:Germany&sensor=false" % location
    combined = url+qs
    attempts = 0
    success = False
    max_attempts = 3

    while success != True and attempts < max_attempts:
        response = requests.get(combined).json()
        attempts += 1
        status = response.get('status')

        if status == "OVER_QUERY_LIMIT":
            logger.debug('API Limit reached. Sleeping 2 seconds')
            time.sleep(2)
            continue

        if status == "ZERO_RESULTS":
            logger.debug("Zero results: %s" % location)
            raise requests.HTTPError()
        success = True
        return response

    if attempts == max_attempts:
        logger.debug("Can't fetch geocoding for: %s" % location)
        raise requests.HTTPError()
