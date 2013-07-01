from django.conf import settings
from django.utils import timezone

from storelocator.models import Location, Shop

from datetime import timedelta
import logging
import yql


logger = logging.getLogger('storelocator')


def yql_request(query):
    """
    Update locations older than x days using YQL.
    """
    API_KEY = getattr(settings, "YQL_API_KEY", None)
    SECRET = getattr(settings, "YQL_CONSUMER_SECRET", None)
    if not API_KEY and not SECRET:
        raise Exception('No api key and secret found.')

    y = yql.TwoLegged(API_KEY, SECRET)

    try:
        result = y.execute(query)
    except yql.YQLError as e:
        raise e

    logger.debug("%s" % query)
    return result


def update_qs_locations(qs, fields, last_updated=None):
    for obj in qs:
        filt = ' '.join([getattr(obj, attr).encode('utf-8') for attr in fields])
        query = "select centroid from geo.places where text='%s'" % filt

        count = 0
        tries = 4

        while True:
            try:
                result = yql_request(query)
            except yql.YQLError as e:
                logger.error(e)
                count += 1
                if count >= tries:
                    raise e
                continue
            break

        try:
            coordinates = result.one()['centroid']
        except IndexError:
            logger.error("Can't fetch query: %s" % filt)
            continue
        except yql.NotOneError:
            coordinates = result.results['place'][0]['centroid']

        new_lat = float(coordinates['latitude'])
        new_lon = float(coordinates['longitude'])

        obj.latitude = new_lat
        obj.longitude = new_lon

        if last_updated:
            obj.last_updated = last_updated
        obj.save()


def yql_update_locations(time_unit, value):
    """
    Use YQL to update locations older than <time unit> <value>.
    """
    now = timezone.now()
    since = now - timedelta(**{time_unit: value})
    locations = Location.objects.filter(last_updated__lte=since)
    update_qs_locations(locations, ['state', 'city', 'postalcode'], now)


def yql_update_shops():
    """
    Use YQL to update shops where longitude and latitude are empty.
    """
    shops = Shop.objects.filter(latitude=None, longitude=None)
    update_qs_locations(shops, ['city', 'postalcode', 'street'])
