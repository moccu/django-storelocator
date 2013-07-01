from django.core.management.base import BaseCommand, CommandError

from storelocator.updaters import google
from storelocator.updaters import yahoo


class Command(BaseCommand):
    help = 'Update shops latitude and longitude with chosen service'

    def handle(self, *args, **kwargs):
        try:
            service = args[0]
        except IndexError:
            raise CommandError('You must provide a service name.')

        if service == "google":
            google.update_shops()
        if service == "yahoo":
            yahoo.yql_update_shops()
        else:
            raise CommandError('You must provide a valid service name.')
