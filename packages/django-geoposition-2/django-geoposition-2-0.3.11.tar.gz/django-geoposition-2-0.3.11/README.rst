==================
django-geoposition
==================
A fork of `django-geoposition`_.

A model field that can hold a geoposition (latitude/longitude), and corresponding admin/form widget.

.. image:: https://badge.fury.io/py/django-geoposition-2.svg
   :target: https://badge.fury.io/py/django-geoposition-2

.. image:: https://travis-ci.org/imdario/django-geoposition.svg?branch=master
   :target: https://travis-ci.org/imdario/django-geoposition


Prerequisites
-------------

Please use from version 0.3.4. Previous versions had several unsolved issues by their original maintainers. django-geoposition requires Django 1.8 or greater.


Installation
------------

- Use your favorite Python packaging tool to install ``geoposition``
  from `PyPI`_, e.g.::

    pip install django-geoposition-2

- Add ``"geoposition"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # …
        "geoposition",
    )

- If you want to use Google Maps, set your Google API key in your settings file::

    GEOPOSITION_GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY'

  API keys may be obtained here: https://developers.google.com/maps/documentation/javascript/get-api-key

- If you want to use OpenStreetMap, activate Leaflet backend in your settings file:

    GEOPOSITION_BACKEND = 'leaflet'

  As Leaflet is provider agnostic, you could use any other map provider from the following list: http://leaflet-extras.github.io/leaflet-providers/preview


Usage
-----

``django-geoposition`` comes with a model field that makes it pretty
easy to add a geoposition field to one of your models. To make use of
it:

- In your ``myapp/models.py``::

    from django.db import models
    from geoposition.fields import GeopositionField

    class PointOfInterest(models.Model):
        name = models.CharField(max_length=100)
        position = GeopositionField()

- This enables the following simple API::

    >>> from geoposition import Geoposition
    >>> from myapp.models import PointOfInterest
    >>> poi = PointOfInterest.objects.create(name='Foo', position=Geoposition(52.522906, 13.41156))
    >>> poi.position
    Geoposition(52.522906,13.41156)
    >>> poi.position.latitude
    52.522906
    >>> poi.position.longitude
    13.41156


Form field and widget
---------------------

Admin
^^^^^

If you use a ``GeopositionField`` in the admin it will automatically
show a `Google Maps`_ widget with a marker at the currently stored
position. You can drag and drop the marker with the mouse and the
corresponding latitude and longitude fields will be updated
accordingly.

It looks like this:

|geoposition-widget-admin|


Regular Forms
^^^^^^^^^^^^^

Using the map widget on a regular form outside of the admin requires
just a little more work. In your template make sure that

- `jQuery`_ is included
- the static files (JS, CSS) of the map widget are included (just use
  ``{{ form.media }}``)

**Example**::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
    <form method="POST" action="">{% csrf_token %}
        {{ form.media }}
        {{ form.as_p }}
    </form>


Settings
--------

You can customize the `MapOptions`_ and `MarkerOptions`_ used to initialize the
map and marker in JavaScript by defining ``GEOPOSITION_MAP_OPTIONS`` or
``GEOPOSITION_MARKER_OPTIONS`` in your ``settings.py``.

**Example**::

    GEOPOSITION_MAP_OPTIONS = {
        'minZoom': 3,
        'maxZoom': 15,
        'parentSelector': 'li.changeform-tabs-item',
        'isDjangoAdmin': True
    }

    GEOPOSITION_MARKER_OPTIONS = {
        'cursor': 'move'
    }

Please note that you cannot use a value like ``new google.maps.LatLng(52.5,13.4)``
for a setting like ``center`` or ``position`` because that would end up as a
string in the JavaScript code and not be evaluated. Please use
`Lat/Lng Object Literals`_ for that purpose, e.g. ``{'lat': 52.5, 'lng': 13.4}``.

You can also customize the height of the displayed map widget by setting
``GEOPOSITION_MAP_WIDGET_HEIGHT`` to an integer value (default is 480).


License
-------

`MIT`_


.. _django-geoposition: https://github.com/philippbosch/django-geoposition
.. _PyPI: http://pypi.python.org/pypi/django-geoposition
.. _Google Maps: http://code.google.com/apis/maps/documentation/javascript/
.. |geoposition-widget-admin| image:: docs/images/geoposition-widget-admin.jpg
.. _jQuery: http://jquery.com
.. _MIT: http://philippbosch.mit-license.org/
.. _MapOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MapOptions
.. _MarkerOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MarkerOptions
.. _Lat/Lng Object Literals: https://developers.google.com/maps/documentation/javascript/examples/map-latlng-literal
