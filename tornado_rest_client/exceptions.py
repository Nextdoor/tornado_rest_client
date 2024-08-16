"""
:mod:`tornado_rest_client.exceptions`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All common exceptions
"""


class BaseFailure(Exception):
    """Base Tornado REST Client Exception"""


class RecoverableFailure(BaseFailure):
    """Base exception that allows calls to be retried"""


class UnrecoverableFailure(BaseFailure):
    """Base exception that prevents any calls from being retried"""


class InvalidOptions(UnrecoverableFailure):
    """Invalid option arguments passed"""


class InvalidCredentials(UnrecoverableFailure):
    """Invalid or missing credentials"""
