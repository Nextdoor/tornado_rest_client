Getting Started
---------------

Setting up your Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create your VirtualEnvironment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ virtualenv .venv --no-site-packages
    New python executable in .venv/bin/python
    Installing setuptools, pip...done.
    $ source .venv/bin/activate

Check out the code
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    (.venv) $ git clone git@github.com:Nextdoor/tornado_rest_client
    Cloning into 'tornado_rest_client'...
    Warning: Permanently added 'github.com,192.30.252.128' (RSA) to the list of known hosts.
    remote: Counting objects: 1831, done.
    remote: irangedCompressing objects: 100% (17/17), done.
    remote: Total 1831 (delta 7), reused 0 (delta 0)
    Receiving objects: 100% (1831/1831), 287.68 KiB, done.
    Resolving deltas: 100% (1333/1333), done.

Install the test-specific dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    (.venv) $ pip install -r tornado_rest_client/requirements.test.txt
    ...
    (.venv) $ cd tornado_rest_client
    (.venv) $ python setup.py test
    ...

Testing
~~~~~~~

Unit Tests
^^^^^^^^^^

The code is 100% unit test coverage complete, and no pull-requests will be
accepted that do not maintain this level of coverage. That said, it's possible
(*likely*) that we have not covered every possible scenario in our unit tests
that could cause failures. We will strive to fill out every reasonable failure
scenario.

Integration Tests
^^^^^^^^^^^^^^^^^

Because it's hard to predict cloud failures, we provide integration tests for
most of our modules. These integration tests actually go off and execute real
operations in your accounts, and rely on particular environments being setup
in order to run.
credentials are all correct.

*Executing the tests*

.. code-block:: bash

    PYFLAKES_NODOCTEST=True python setup.py integration pep8 pyflakes

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
