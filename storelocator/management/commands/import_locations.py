from django.core.management.base import BaseCommand, CommandError

from storelocator.importers import locations


class Command(BaseCommand):
    help = 'Imports locations from geonames.org'

    def handle(self, *args, **kwargs):
        try:
            path = args[0]
        except IndexError:
            raise CommandError('You must provide a path for your csv file.')

        importer = locations.GeonamesLocationImporter(path, dialect='excel-tab')
        importer.run()
