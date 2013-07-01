=====
Usage
=====

Read here how to use Storelocator after installing.

Data sources
------------

The Storelocator depends on external data.

Data for the ``Shop`` model can be provided for by the user.

Data for the ``Location`` model can be imported from third party sources. Locations are needed
in case the API is called with a postalcode. In this situation the center position
is the center position of the postalcode area.

We recommend Geonames as an external datasource for our ``Location`` models.
This data can be downloaded from `Geonames <http://download.geonames.org/export/zip/>`_
in csv format.


Management commands
-------------------

The available management commands are listed here.

import_locations <file>
~~~~~~~~~~~~~~~~~~~~~~~

Imports locations from a geonames csv file.

Example usage::

    django-admin.py import_locations locations.csv


import_shops <file> <storelocator_id>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imports shops from a csv file. The csv file needs to have the following field
order:

``type``, ``name``, ``street``, ``postalcode``, ``city``, ``state``, ``iso``

You also have to store a ``StoreLocator`` object to the database before creating shops.
The id of your object should be used as a second argument for this management command.

Example usage::

    django-admin.py import_shops shops.csv 1


update_shops <service>
~~~~~~~~~~~~~~~~~~~~~~

Updates the ``longitude`` and ``latitude`` fields on ``Shop`` objects by using
your service of choice.

The services you can choose are:

- ``google`` This uses Google's Geocoding API.
- ``yahoo`` This uses Yahoo's yql.

Example usage::

    django-admin.py update_shops yahoo

Note:
    Currently the google variant does not support authentication and supports
    only 2500 requests a day.


update_locations <time unit> <days> <service>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates the ``longitude`` and ``latitude`` fields on ``Location`` objects since
``timedelta time unit`` ``value``. Only supports Yahoo's yql at the moment.

Example usage::

    django-admin.py update_locations minutes 30 yahoo
    django-admin.py update_locations days 10 yahoo
    django-admin.py update_locations months 1 yahoo


API
---

``http://localhost:8000/storelocator/<slug>.json?parameters``


Filter by Postalcode
~~~~~~~~~~~~~~~~~~~~

Required parameters:

- ``postalcode``
- ``iso``

``http://localhost:8000/storelocator/test-storelocator.json?postalcode=5271&iso=NL``
::

    {
        "non_field_errors": [],
        "form_errors": {},
        "shops": [
            {
                "city": "Maaskantje",
                "name": "Cafetaria ‘t Pleintje",
                "distance": false,
                "longitude": 5.37346,
                "latitude": 51.66718,
                "street": "Pilotenstraat",
                "postalcode": "5275 BA",
                "type": "snackbar"
            }
        ],
        "success": true
    }

Filter by Longitude and Latitude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required parameters:

- ``longitude``
- ``latitude``

``http://localhost:8000/storelocator/test-storelocator.json?longitude=5.37148&latitude=51.66599``
::

    {
        "non_field_errors": [],
        "form_errors": {},
        "shops": [
            {
                "city": "Maaskantje",
                "name": "Cafetaria ‘t Pleintje",
                "distance": 0.1,
                "longitude": 5.37346,
                "latitude": 51.66718,
                "street": "Pilotenstraat",
                "postalcode": "5275 BA",
                "type": "snackbar"
            }
        ],
        "success": true
    }


Extra filters / parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

Required parameters:

- ``callback=jsonp``

    Adds json padding.

- ``language=nl``

    Changes the language of error messages in the response.

    This parameter only works if the language has been set in
    ``settings.LANGUAGES`` and the translation files are available.

- ``limit=5``

    Limits the shop results to a given number.

    If the value of ``limit`` is set to ``0``, the shop results will be empty.

- ``radius=3.0``

    Changes the lookup radius of shops nearby the centerpoint of your
    postalcode or longitude and latitude.

    The minimum value of ``radius`` is  ``0.1``.