Simple API Access Objects
~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the APIs out there leverage basic REST with JSON or XML as the data
encoding method. Since these APIs behave similarly, we have created a simple
API access object that can be extended for creating actors quickly.  The object
is called a ``RestConsumer`` and is in the ``kingpin.actors.support.api`` package.
This ``RestConsumer`` can be subclassed and filled in with a ``dict`` that
describes the API in detail.

HTTPBin Actor with the RestConsumer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    HTTPBIN = {
        'path': '/',
        'http_methods': {'get': {}},
        'attrs': {
            'get': {
                'path': '/get',
                'http_methods': {'get': {}},
            },
            'post': {
                'path': '/post',
                'http_methods': {'post': {}},
            },
            'put': {
                'path': '/put',
                'http_methods': {'put': {}},
            },
            'delete': {
                'path': '/delete',
                'http_methods': {'delete': {}},
            },
        }
    }


    class HTTPBinRestClient(api.RestConsumer):

        CONFIG = HTTPBIN
        ENDPOINT = 'http://httpbin.org'


    class HTTPBinGetThenPost(base.BaseActor):
        def __init__(self, \*args, \**kwargs):
            super(HTTPBinGetThenPost, self).__init__(\*args, \**kwargs)
            self._api = HTTPBinRestClient()

        @gen.coroutine
        def _execute(self):
            yield self._api.get().http_get()

            if self._dry
                raise gen.Return()

            yield self._api.post().http_post(foo='bar')

            raise gen.Return()

Exception Handling in HTTP Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``RestClient.fetch()`` method has been wrapped in a ``retry decorator`` that
allows you to define different behaviors based on the exceptions returned from
the fetch method. For example, you may want to handle an HTTPError exception
with a ``401`` error code differently than a ``503`` error code.

You can customize the exception handling by subclassing the
``RestClient``:

.. code-block:: python

    class MyRestClient(api.RestClient):
        EXCEPTIONS = {
            httpclient.HTTPError: {
                '401': my.CustomException(),
                '403': exceptions.InvalidCredentials,
                '500': my.UnretryableError(),
                '502': exceptions.InvalidOptions,

                # This acts as a catch-all
                '': exceptions.RecoverableActorFailure,
            }
        }
