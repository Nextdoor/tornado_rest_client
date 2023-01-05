"""
:mod:`tornado_rest_client.utils`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Common package for utility functions.
"""

import logging
import re

from tornado import gen

__author__ = "Matt Wise (matt@nextdoor.com)"

log = logging.getLogger(__name__)


@gen.coroutine
def tornado_sleep(seconds=1.0):
    """Async method equivalent to sleeping.

    Args:
        seconds: Float seconds. Default 1.0
    """
    yield gen.sleep(seconds)


def populate_with_tokens(string, tokens, left_wrapper="%", right_wrapper="%", strict=True):
    """Insert token variables into the string.

    Will match any token wrapped in '%'s and replace it with the value of that
    token.

    Args:
        string: string to modify.
        tokens: dictionary of key:value pairs to inject into the string.
        left_wrapper: the character to use as the START of a token
        right_wrapper: the character to use as the END of a token
        strict: (bool) whether or not to make sure all tokens were replaced

    Example:
        export ME=biz

        string='foo %ME% %bar%'
        populate_with_tokens(string, os.environ)  # 'foo biz %bar%'
    """

    # First things first, swap out all instances of %<str>% with any matching
    # token variables found. If no items are in the hash (none, empty hash,
    # etc), then skip this.
    allowed_types = (str, bool, int, float)
    if tokens:
        for key, val in tokens.items():

            if type(val) not in allowed_types:
                log.warning("Token %s=%s is not in allowed types: %s", key, val, allowed_types)
                continue

            string = string.replace(f"{left_wrapper}{key}{right_wrapper}", str(val))

    # If we aren't strict, we return...
    if not strict:
        return string

    # If we are strict, we check if we missed anything. If we did, raise an
    # exception.
    missed_tokens = list(set(re.findall(rf"{left_wrapper}[\w]+{right_wrapper}", string)))
    if missed_tokens:
        raise LookupError(f"Found un-matched tokens in JSON string: {missed_tokens}")

    return string
