from .importer import UnicodeCSVImporter
from storelocator.models import Shop, StoreLocator


class ShopImporter(UnicodeCSVImporter):

    """
    Imports shops in a custom format.
    First row needs the following fields:
        type, name, street, postalcode, city, state, iso
    """

    def run(self, storelocator_id):
        try:
            storelocator = StoreLocator.objects.get(id=storelocator_id)
        except StoreLocator.DoesNotExist:
            raise Exception(
                "Can't find StoreLocator object with id: %i" % storelocator_id)

        data_map = {
            "type": 0,
            "name": 1,
            "street": 2,
            "postalcode": 3,
            "city": 4,
            "state": 5,
            "iso": 6
        }

        # get rid of double entries
        rows = set(map(tuple, self.rows))

        # save shops
        bulk_objects = []
        for m in rows:
            bulk_objects.append(
                Shop(
                    type = m[data_map["type"]],
                    name = m[data_map["name"]],
                    city = m[data_map["city"]],
                    postalcode = m[data_map["postalcode"]],
                    street = m[data_map["street"]],
                    iso = m[data_map["iso"]],
                    storelocator_id = storelocator.id))

        Shop.objects.bulk_create(bulk_objects)