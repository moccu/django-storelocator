from django.core.management.base import BaseCommand, CommandError

from storelocator.updaters import yahoo


class Command(BaseCommand):

    help = (
        "Update existing locations with latitude and longitude chosen service")

    def handle(self, *args, **kwargs):
        try:
            time_unit = args[0]
        except IndexError:
            raise CommandError('Choose a timedelta time_unit.')

        try:
            value = int(args[1])
        except IndexError:
            raise CommandError('You must provide a time value.')

        try:
            service = args[2]
        except IndexError:
            raise CommandError('You must provide a service name.')

        if service == "yahoo":
            yahoo.yql_update_locations(time_unit, value)
        else:
            raise CommandError('You must provide a valid service name.')
