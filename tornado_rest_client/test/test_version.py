"""Vanity test"""

import unittest

import six
import six.moves


class TestVersion(unittest.TestCase):

    def test_version(self):
        from tornado_rest_client import version
        six.moves.reload_module(version)
        self.assertIsInstance(version.__version__, six.string_types)
