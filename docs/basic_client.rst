Simple API Access Objects
~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the APIs out there leverage basic REST with JSON or XML as the data
encoding method. Since these APIs behave similarly, we can define the API
URLs and HTTP methods inside a `dict`, without writing any actual python 
methods.

HTTPBin RestConsumer
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


    class HTTPBinGetThenPost(object):
        def __init__(self, \*args, \**kwargs):
            super(HTTPBinGetThenPost, self).__init__(\*args, \**kwargs)
            self._api = HTTPBinRestClient()

        @gen.coroutine
        def execute(self):
            yield self._api.get().http_get()
            yield self._api.post().http_post(foo='bar')

Exception Handling in HTTP Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :func:`~tornado_rest_client.api.RestClient.fetch` method has been wrapped
in a :func:`~tornado_rest_client.api.retry` decorator that allows you to
define different behaviors based on the exceptions returned from the fetch
method. For example, you may want to handle an
:exc:`~tornado_rest_client.httpclient.HTTPError` exception with a ``401``
error code differently than a ``503`` error code.

You can customize the exception handling by subclassing the
:class:`~tornado_rest_client.api.RestClient`:

.. code-block:: python

    class MyRestClient(api.RestClient):
        EXCEPTIONS = {
            httpclient.HTTPError: {
                # These do not retry, they immediately raise an exception
                '401': my.CustomException(),
                '403': exceptions.InvalidCredentials,
                '500': my.UnretryableError(),
                '502': exceptions.InvalidOptions,

                # This indicates a retry should happen
                '503': None, 

                # This acts as a catch-all
                '': MyException,
            }
        }
