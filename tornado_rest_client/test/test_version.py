"""Vanity test"""

import unittest


class TestVersion(unittest.TestCase):

    def test_version(self):
        from tornado_rest_client import version
        reload(version)
        self.assertEquals(type(version.__version__), str)
