"""Vanity test"""

import unittest

try:
    from importlib import reload
except ImportError:
    # py3 specific only
    pass


class TestVersion(unittest.TestCase):

    def test_version(self):
        from tornado_rest_client import version
        reload(version)
        self.assertEquals(type(version.__version__), str)
