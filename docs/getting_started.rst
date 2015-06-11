Getting Started
---------------

Getting started with `tornado_rest_client` is easy.

 * Define the API methods you plan to support
 * Build any custom functions that you need
 * Ship it!

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
