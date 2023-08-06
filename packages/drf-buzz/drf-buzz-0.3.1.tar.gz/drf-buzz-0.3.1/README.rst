|Build Status| |Coverage Status|

drf-buzz
========

This is an extension of the `py-buzz`_ package.

It adds extra functionality especially for DRF. Predominately, it adds
the ability to jsonify an exception

Installation
------------

::

   pip install drf-buzz

Usage
-----

Add ``drf-buzz`` exception handler in ``settings.py``:

.. code:: python

   REST_FRAMEWORK = {
       ...
       'EXCEPTION_HANDLER': 'drf_buzz.exception_handler'
       ...
   }

Use ``py-buzz`` exceptions in your DRF viewsets:

.. code:: python

   import drf_buzz

   from rest_framework import status, viewsets


   class MyException(drf_buzz.DRFBuzz):
       status_code = status.BAD_REQUEST


   class MyViewSet(viewsets.ViewSet):
       def list(self, request):
           raise MyException('Not implemented yet.')

Tests
-----

To run the test suite execute the following command in package root
folder:

::

   python setup.py test

.. _py-buzz: https://github.com/dusktreader/py-buzz

.. |Build Status| image:: https://travis-ci.org/adalekin/drf-buzz.svg?branch=master
   :target: https://travis-ci.org/adalekin/drf-buzz
.. |Coverage Status| image:: https://coveralls.io/repos/github/adalekin/drf-buzz/badge.svg?branch=master
   :target: https://coveralls.io/github/adalekin/drf-buzz?branch=master