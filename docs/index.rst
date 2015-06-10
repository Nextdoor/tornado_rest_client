Tornado API Client Framework
============================

The `tornado_rest_client` framework provides a quick and easy way to build
generic API clients for JSON REST-based APIs. The framework provides robust
and reliable retry mechanisms, error handling and exception raising all within
a simple to use class structure.

The basic purpose of the :mod:`~tornado_rest_client.api` package is to
provide you with a few simple inheritable classes where all you need to do is
fill in a few variables to get back a usable API client.

Every API client you build will be a combination of two objects -- a
:class:`~tornado_rest_client.api.RestClient` and a
:class:`~tornado_rest_client.api.RestConsumer`.

RestClient
----------

A `RestClient` object is a very simple object that exposes one public
:func:`~tornado_rest_client.api.RestClient.fetch` method (that's wrapped in
the `tornado.gen.coroutine` wrapper) used to fire off HTTP calls through a
`tornado.httpclient.AsyncHTTPClient` object.

.. toctree::
   :maxdepth: 2

   getting_started
   basic_client
   modules

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

