from django.core.management.base import BaseCommand, CommandError

from storelocator.importers import shops


class Command(BaseCommand):
    help = 'Imports shops from csv'

    def handle(self, *args, **kwargs):
        try:
            path = args[0]
        except IndexError:
            raise CommandError('You must provide a path for your csv file.')

        try:
            storelocator_id = args[1]
        except IndexError:
            raise CommandError('You must provide the id of a storelocator obj')

        importer = shops.ShopImporter(path, dialect='excel-tab', delimiter=',')
        importer.run(storelocator_id)
