import os
import unittest

from tornado_rest_client import utils


class TestUtils(unittest.TestCase):
    def test_populate_with_env(self):
        tokens = {"UNIT_TEST": "FOOBAR"}
        string = "Unit %UNIT_TEST% Test"
        expect = "Unit FOOBAR Test"
        result = utils.populate_with_tokens(string, tokens)
        self.assertEqual(result, expect)

    def test_populate_with_unicode_env(self):
        tokens = {"UNIT_TEST": "FOOBAR"}
        string = "Unit %UNIT_TEST% Test"
        expect = "Unit FOOBAR Test"
        result = utils.populate_with_tokens(string, tokens)
        self.assertEqual(result, expect)

    def test_populate_with_bool(self):
        tokens = {"UNIT_TEST": True}
        string = "Unit %UNIT_TEST% Test"
        expect = "Unit True Test"
        result = utils.populate_with_tokens(string, tokens)
        self.assertEqual(result, expect)

    def test_populate_with_bogus_data_OK(self):
        tokens = {"UNIT_TEST": {"foobar": "bat"}}
        string = "Unit %UNIT_TEST% Test"
        expect = "Unit %UNIT_TEST% Test"
        result = utils.populate_with_tokens(string, tokens, strict=False)
        self.assertEqual(result, expect)

    def test_populate_with_env_with_missing_variables(self):
        os.environ["UNIT_TEST"] = "FOOBAR"
        string = "Unit %UNIT_TEST% Test %NOTFOUNDVARIABLE%"
        with self.assertRaises(LookupError):
            utils.populate_with_tokens(string, os.environ)

    def test_populate_with_env_with_non_string_tokens(self):
        tokens = {"foo": False}
        string = "Unit test"
        result = utils.populate_with_tokens(string, tokens)
        self.assertEqual(result, string)

    def test_populate_with_not_strict(self):
        tokens = {"UNIT_TEST": "FOOBAR"}
        string = "Unit {UNIT_TEST} {FAIL} Test"
        expect = "Unit FOOBAR {FAIL} Test"
        result = utils.populate_with_tokens(
            string, tokens, left_wrapper="{", right_wrapper="}", strict=False
        )
        self.assertEqual(result, expect)
