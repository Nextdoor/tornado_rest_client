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

A :class:`~tornado_rest_client.api.RestClient` object is a very simple object
that exposes one public :func:`~tornado_rest_client.api.RestClient.fetch`
method (that's wrapped in the :func:`~tornado.gen.coroutine` wrapper) used to
fire off HTTP calls through a :class:`tornado.httpclient.AsyncHTTPClient`
object.

RestConsumer
------------

The :class:`~tornado_rest_client.api.RestConsumer` class does the real leg
work. At the root of it, the object self-configures itself with a supplied
:attr:`~tornado_rest_client.api.RestConsumer.CONFIG` dictionary that defines
`http_methods`, `path` and possible `attrs`. The `http_methods` and `path` work
together to tell the object exactly what path it will call out to, and what
methods it supports. The `attrs` provide links to nested methods that return
other :class:`~tornado_rest_client.api.RestConsumer` objects.

If you consider an API that may have the following endpoints:

 * **GET /**: Returns 200 if API is up
 * **GET /cats**: Returns a `array` of cat names
 * **POST /cats**: Push a new name to the `array` of cat names
 * **GET /cats/random**: Returns a single random cat name

You can define your :attr:`~tornado_rest_client.api.RestConsumer.CONFIG` dict
like this:

.. code-block:: python

    class CatAPI(api.RestConsumer):
        ENDPOINT = 'http://my_cat_service'
        CONFIG = {
            # Handles GET /
            'path': '/',
            'http_methods': {'get': {}},
            # Creates a series of methods that return other RestConsumers
            'attrs': {
                # Handles GET /cats, POST /cats
                'cat_api': {
                    'path': '/cats',
                    'http_methods': {
                        'get': {},
                        'post': {},
                    },
                    # Now, handles the random cat endpoint
                    'attrs': {
                        'random': {
                            'path': '/cats/random',
                            'http_methods': {
                                'get': {}
                            }
                        }
                    }
                }
            }
        }

Now, instantiating this object would provide methods that look like this:

.. code-block:: python

    >>> cats = CatAPI()
    >>> cats
    CatAPI(/)
    >>> cats.cat_api()
    CatAPI(/cats)
    >>> cats.cat_api().random()
    CatAPI(/cats/random)
    >>> cats.cat_api().random().http_get()
    <tornado.concurrent.Future object at 0x101f9e390>
    >>> yield cats.cat_api().random().http_get()
    'Bob Marley!'
    >>> yield cats.cat_api().http_post(cat_name='Skippy')
    { "status": "ok" }

There are more details available inside the various doc modules below...

.. toctree::
   :maxdepth: 2

   getting_started
   basic_client
   modules

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

