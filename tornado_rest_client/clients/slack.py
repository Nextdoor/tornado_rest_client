"""
:mod:`tornado_rest_client.clients.slack`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A simple Slack API client that provides basic message sending capabilities.
Note, many more functions can be added to this class, but initially its very
simple.

Usage:

    >>> api = slack.Slack(token='unittest')
    >>> auth_ok = yield api.auth_test().http_post()
    >>> print('Auth OK? %s' % api.check_results(auth_ok))
    >>> ret = yield api.chat_postMessage().http_post(
    ...     channel='#systems',
    ...     text='This is a test message',
    ...     username='Matt',
    ...     parse='none',
    ...     link_names=1,
    ...     unfurl_links=True,
    ...     unfurl_media=True)
    >>> print ('Message sent? %s' % api.check_results(ret))

.. autoclass:: Slack
   :members:
   :inherited-members:
   :show-inheritance:
"""

import logging

log = logging.getLogger(__name__)

from tornado_rest_client import api, exceptions


class RequestFailure(exceptions.BaseFailure):
    """Failure to parse the return data from Slack."""


class Error(exceptions.BaseFailure):
    """Failure to execute API call returned by Slack."""


class Slack(api.RestConsumer):
    """Simple Slack API Client.

    This example API client has very limited functionality -- basically it
    implements the `/api/auth.test` and `/api/chat.postMessage` functions.

    .. py:method:: auth_test

        Accesses https://api.slack.com/api/auth.test

        .. py:method:: http_post

    .. py:method:: chat_postMessage

        Accesses https://api.slack.com/api/chat.postMessage

        .. py:method:: http_post(channel, text, username[, as_user, parse,
            link_names, attachments, unfurl_links, unfurl_media, icon_url,
            icon_emoji])
    """

    ENDPOINT = "https://api.slack.com"
    CONFIG = {
        "attrs": {
            "auth_test": {
                "path": "/api/auth.test",
                "http_methods": {"post": {}},
            },
            "chat_postMessage": {
                "path": "/api/chat.postMessage",
                "http_methods": {"post": {}},
            },
        }
    }

    def __init__(self, *args, **kwargs):
        if "token" not in kwargs:
            raise exceptions.InvalidCredentials('Missing "token" keyword argument.')

        kwargs["client"] = api.SimpleTokenRestClient(tokens={"token": kwargs["token"]})

        super().__init__(*args, **kwargs)

    def check_results(self, result):
        """Returns True/False if the result was OK from Slack.

        The Slack API avoids using standard error codes, and instead embeds
        error codes in the return results. This method returns True or False
        based on those results.

        :param dict result: A return dict from Slack

        :raises InvalidCredentials: if the creds are bad
        :raises Error: exception on any other value
        :raises RequestFailure: response with no `ok` field
        :return: If the API call succeeded or failed without error
        :rtype: bool
        """
        try:
            if result.get("ok", False):
                return True

            error = result["error"]
        except (AttributeError, KeyError) as e:
            raise RequestFailure(
                f"An unexpected Slack API failure occured: {result}"
            ) from e

        if error == "invalid_auth":
            raise exceptions.InvalidCredentials(f'Slack API Error: "invalid_auth".')

        raise Error(f"Slack API Error: {error}")
