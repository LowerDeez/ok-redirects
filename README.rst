==================================
django-ok-redirects |PyPI version|
==================================

|Upload Python Package| |Code Health| |Python Versions| |PyPI downloads| |license| |Project Status|

Simple Redirects App, which is particularly useful in the cases where you want to update some existing URLs without compromising your Website SEO.

Installation
============

Install with pip:

.. code:: shell

    $ pip install django-ok-redirects

Update INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...
        'ok_redirects',
        ...
    ]

Make migrations

.. code:: shell

    $ python manage.py migrate


Available settings
==================

``REDIRECTS_IGNORE_PATH_PREFIXES`` - Tuple of path prefixes to ignore.


For example:

.. code:: python

    REDIRECTS_IGNORE_PATH_PREFIXES = (
        '/api/v1/',
        '/uploads/',
        '/static/',
    )


Basic example to use:
=====================

Add the redirects middleware to the MIDDLEWARE configuration:
-------------------------------------------------------------

.. code:: python

    MIDDLEWARE = [
        ...

        'ok_redirects.middleware.RedirectMiddleware'
    ]


.. |PyPI version| image:: https://badge.fury.io/py/django-ok-redirects.svg
   :target: https://badge.fury.io/py/django-ok-redirects
.. |Upload Python Package| image:: https://github.com/LowerDeez/ok-redirects/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/LowerDeez/ok-redirects/
   :alt: Build status
.. |Code Health| image:: https://api.codacy.com/project/badge/Grade/e5078569e40d428283d17efa0ebf9d19
   :target: https://www.codacy.com/app/LowerDeez/ok-redirects
   :alt: Code health
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/django-ok-redirects.svg
   :target: https://pypi.org/project/django-ok-redirects/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-ok-redirects.svg
   :alt: Software license
   :target: https://github.com/LowerDeez/ok-redirects/blob/master/LICENSE
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/django-ok-redirects.svg
   :alt: PyPI downloads
.. |Project Status| image:: https://img.shields.io/pypi/status/django-ok-redirects.svg
   :target: https://pypi.org/project/django-ok-redirects/  
   :alt: Project Status
