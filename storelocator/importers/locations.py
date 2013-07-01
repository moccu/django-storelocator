from .importer import UnicodeCSVImporter
from storelocator.models import Location


class GeonamesLocationImporter(UnicodeCSVImporter):

    """
    Imports locations from http://download.geonames.org/export/zip/
    """

    def run(self):
        bulk_objects = []

        for row in self.rows:
            bulk_objects.append(
                Location(
                    iso=row[0],
                    postalcode=row[1],
                    city=row[2],
                    state=row[3],
                    latitude=row[9],
                    longitude=row[10]))

        Location.objects.bulk_create(bulk_objects)
