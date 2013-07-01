============
Installation
============


Pip
===

* Install Django Storelocator::

    pip install django-storelocator

* Add ``'storelocator'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        "storelocator",
    )

* Run syncdb and run south migrations::

    ./manage.py syncdb --migrate

* Add the app to your url conf::

    url(r'^storelocator/', include('storelocator.urls')),


Running Tests
=============

*For Django <= 1.5.1*

If you want to run the tests of the Django Storelocator, follow these steps:

* Create a new virtualenv to work in.

* Install the package with the ``--editable`` option::

    pip install -e git+https://github.com/moccu/django-storelocator.git

* Install dependencies for the tests::

    pip install Django == 1.5.1
    pip install django-discover-runner >= 0.4
    pip install mock >= 1.0.1
    pip install factory-boy >= 1.2.0

* Go to the directory where the package is stored and run::

    django-admin.py test --settings=storelocator.tests.testsettings