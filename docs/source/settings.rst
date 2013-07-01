========
Settings
========

.. currentmodule:: django.conf.settings

The Django settings for the Django Storelocator.


Settings: YQL
-------------

Sometimes geographical data changes and needs to be updated, because the data
isn't stale or your data source has inaccuracies.

Django Storelocator comes with management commands to update the Location or
Shop models latitude and longitude properties.


.. attribute:: YQL_API_KEY

    :type: string
    :default: None

    The API key of your Yahoo YQL app.


.. attribute:: YQL_CONSUMER_SECRET

    :type: string
    :default: None

    The API consumer secret of your Yahoo YQL app.


Settings: General settings
--------------------------

Django Storelocator general settings all have default values and don't
necessarily need to be changed.

.. attribute:: STORELOCATOR_RADIUS_MAX

    :type: float (km)
    :default: 10.0
    :min: 0

    Sets the maximum radius.


.. attribute:: STORELOCATOR_LIMIT_MAX

    :type: int
    :default: 15
    :min: 0

    Sets the max value on shop results that can be listed in the response.


Logger
------

You can optionally add the ``'storelocator'`` logger to your loggers::

    # example
    ...
    'storelocator': {
       'handlers': ['file','console'],
       'level': 'DEBUG',
       'propagate': False,
    },


Language support
----------------

If you want to determine the language by requesters client, add the ``LocaleMiddleware``
middleware to ``MIDDLEWARE_CLASSES`` in your settings.

::

    MIDDLEWARE_CLASSES = (
        ...
        'django.middleware.locale.LocaleMiddleware',
    )