"""Tests for the actors.base package."""

import mock

from tornado import gen, httpclient, testing

from tornado_rest_client import api, exceptions


@gen.coroutine
def tornado_value(value=None):
    """Converts whatever is passed in to a tornado value."""
    raise gen.Return(value)


class RestClientTest(api.RestClient):
    """Fake web client object for unit tests."""

    @gen.coroutine
    @api.retry
    def fetch(self, url, method, params={}, auth_username=None, auth_password=None):
        # Turn all the iputs into a JSON dict and return them
        ret = {
            "url": url,
            "method": method,
            "params": params,
            "auth_username": auth_username,
            "auth_password": auth_password,
        }
        raise gen.Return(ret)


class RestConsumerTest(api.RestConsumer):

    CONFIG = {
        "attrs": {
            "testA": {
                "path": "/testA",
                "http_methods": {
                    "get": {},
                    "post": {},
                    "put": {},
                    # Note, 'delete' specifically avoided
                },
            },
            "test_path_with_res": {
                "path": "/test/%res%/info",
                "http_methods": {"get": {}},
            },
            "test_path_with_new_access_type": {
                "path": "/test/new",
                "new": True,
                "http_methods": {"get": {}},
            },
            "test_path_with_new_access_type_with_res": {
                "path": "/test/%res/new",
                "new": True,
                "http_methods": {"get": {}},
            },
        }
    }
    ENDPOINT = "http://unittest.com"


class RestConsumerTestBasicAuthed(RestConsumerTest):
    CONFIG = dict(RestConsumerTest.CONFIG)
    CONFIG["auth"] = {"user": "username", "pass": "password"}


class TestRetry(testing.AsyncTestCase):
    @testing.gen_test
    def test_decorator_plain(self):
        class TestException(Exception):
            pass

        class FailingClass:
            """Test class that is intended for @retry decorator"""

            EXCEPTIONS = {TestException: {"cruel": None}}  # Retry during cruelty

            _call_count = 0

            @gen.coroutine
            @api.retry
            def func(self):
                self._call_count = self._call_count + 1
                raise TestException("Goodbye cruel world...")

        fail = FailingClass()

        with self.assertRaises(TestException):
            yield fail.func()

        self.assertEqual(fail._call_count, 3)

    @testing.gen_test
    def test_decorator_with_args(self):
        class TestException(Exception):
            pass

        class FailingClass:
            """Test class that is intended for @retry decorator"""

            EXCEPTIONS = {TestException: {"cruel": None}}  # Retry during cruelty

            _call_count = 0

            @gen.coroutine
            @api.retry(delay=0, retries=7)
            def func(self):
                self._call_count = self._call_count + 1
                raise TestException("Goodbye cruel world...")

        fail = FailingClass()

        with self.assertRaises(TestException):
            yield fail.func()

        self.assertEqual(fail._call_count, 7)


class TestRestConsumer(testing.AsyncTestCase):
    @testing.gen_test
    def test_object_attributes(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        self.assertEqual(test_consumer.__repr__(), "RestConsumerTest(None)")
        self.assertEqual(test_consumer.testA().__repr__(), "RestConsumerTest(/testA)")

    @testing.gen_test
    def test_replace_path_tokens(self):
        test_consumer = RestConsumerTest(client=RestClientTest())

        # with missing 'res' arg, it should fail
        with self.assertRaises(TypeError):
            test_consumer.test_path_with_res()

        # with arg, it should pass
        ret = test_consumer.test_path_with_res(res="abcd")
        self.assertEqual(str(ret), "/test/abcd/info")

    @testing.gen_test
    def test_new_style_path_with_property_access(self):
        test_consumer = RestConsumerTest(client=RestClientTest())

        # the path with an arg must exist as an access method, and fail if you
        # don't supply the arg.
        self.assertFalse(
            callable(test_consumer.test_path_with_new_access_type_with_res)
        )

        # with arg, it should pass
        ret = test_consumer.test_path_with_new_access_type
        self.assertEqual(str(ret), "/test/new")

    @testing.gen_test
    def test_http_method_get(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        ret = yield test_consumer.testA().http_get()
        expected_ret = {
            "url": "http://unittest.com/testA",
            "params": {},
            "auth_password": None,
            "auth_username": None,
            "method": "GET",
        }
        self.assertEqual(ret, expected_ret)

    @testing.gen_test
    def test_http_method_get_with_basic_auth(self):
        test_consumer = RestConsumerTestBasicAuthed(client=RestClientTest())
        ret = yield test_consumer.testA().http_get()
        expected_ret = {
            "url": "http://unittest.com/testA",
            "params": {},
            "auth_password": "password",
            "auth_username": "username",
            "method": "GET",
        }
        self.assertEqual(ret, expected_ret)

    @testing.gen_test
    def test_http_method_get_with_args(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        with self.assertRaises(exceptions.InvalidOptions):
            yield test_consumer.testA().http_get("foo")

    @testing.gen_test
    def test_http_method_post(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        ret = yield test_consumer.testA().http_post(foo="bar")
        expected_ret = {
            "url": "http://unittest.com/testA",
            "params": {"foo": "bar"},
            "auth_password": None,
            "auth_username": None,
            "method": "POST",
        }
        self.assertEqual(ret, expected_ret)

    @testing.gen_test
    def test_http_method_put(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        ret = yield test_consumer.testA().http_put(foo="bar")
        expected_ret = {
            "url": "http://unittest.com/testA",
            "params": {"foo": "bar"},
            "auth_password": None,
            "auth_username": None,
            "method": "PUT",
        }
        self.assertEqual(ret, expected_ret)

    @testing.gen_test
    def test_http_method_delete(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        with self.assertRaises(AttributeError):
            yield test_consumer.testA().http_delete()

    @testing.gen_test
    def test_http_get_with_args(self):
        test_consumer = RestConsumerTest(client=RestClientTest())
        with self.assertRaises(exceptions.InvalidOptions):
            yield test_consumer.testA().http_get("bar")


class TestRestClient(testing.AsyncTestCase):
    def setUp(self, *args, **kwargs):
        super(TestRestClient, self).setUp()
        self.client = api.RestClient()
        self.http_response_mock = mock.MagicMock(name="response")
        self.http_client_mock = mock.MagicMock(name="http_client")
        self.http_client_mock.fetch.return_value = tornado_value(
            self.http_response_mock
        )
        self.client._client = self.http_client_mock

    def test_init_content_type(self):
        client = api.RestClient(json=True)
        self.assertEqual(client.headers, {"Content-Type": "application/json"})

    @testing.gen_test
    def test_generate_escaped_url(self):
        result = self.client._generate_escaped_url("http://unittest", {"foo": "bar"})
        self.assertEqual("http://unittest?foo=bar", result)
        result = self.client._generate_escaped_url("http://unittest", {"foo": True})
        self.assertEqual("http://unittest?foo=true", result)
        result = self.client._generate_escaped_url(
            "http://unittest", {"foo": "bar", "xyz": "abc"}
        )
        self.assertEqual("http://unittest?foo=bar&xyz=abc", result)
        result = self.client._generate_escaped_url(
            "http://unittest", {"foo": "bar baz", "xyz": "abc"}
        )
        self.assertEqual("http://unittest?foo=bar+baz&xyz=abc", result)

    @testing.gen_test
    def test_fetch_post_with_args(self):
        self.http_response_mock.body = '{"foo": "bar"}'
        ret = yield self.client.fetch(
            url="http://foo.com", method="POST", params={"foo": "bar", "baz": "bat"}
        )
        self.assertEqual({"foo": "bar"}, ret)
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_post_with_args_and_json_body(self):
        self.http_response_mock.body = '{"foo": "bar"}'
        self.client.JSON_BODY = True
        ret = yield self.client.fetch(
            url="http://foo.com", method="POST", params={"foo": "bar", "baz": "bat"}
        )
        self.assertEqual({"foo": "bar"}, ret)
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_get_with_args(self):
        self.http_response_mock.body = '{"foo": "bar"}'
        ret = yield self.client.fetch(
            url="http://foo.com", method="GET", params={"foo": "bar", "baz": "bat"}
        )
        self.assertEqual({"foo": "bar"}, ret)
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_get_returns_json(self):
        self.http_response_mock.body = '{"foo": "bar"}'
        ret = yield self.client.fetch(url="http://foo.com", method="GET")
        self.assertEqual({"foo": "bar"}, ret)
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_get_returns_string(self):
        self.http_response_mock.body = "foo bar"
        ret = yield self.client.fetch(url="http://foo.com", method="GET")
        self.assertEqual("foo bar", ret)
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_401_raises_exc_and_called_once(self):
        e = httpclient.HTTPError(401, "Unauthorized")
        self.http_client_mock.fetch.side_effect = e
        with self.assertRaises(exceptions.InvalidCredentials):
            yield self.client.fetch(url="http://foo.com", method="GET")
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_unexpected_failure_raises_exc_and_called_once(self):
        # Wipe out the 'default' http error handling config for this test.
        self.client.EXCEPTIONS = {httpclient.HTTPError: {}}
        e = httpclient.HTTPError(300, "Unexpected")
        self.http_client_mock.fetch.side_effect = e
        with self.assertRaises(httpclient.HTTPError):
            yield self.client.fetch(url="http://foo.com", method="GET")
        self.http_client_mock.fetch.assert_called_once()

    @testing.gen_test
    def test_fetch_500_raises_exc_and_called_many_times(self):
        e = httpclient.HTTPError(500, "Failure")
        self.http_client_mock.fetch.side_effect = e
        with self.assertRaises(httpclient.HTTPError):
            yield self.client.fetch(url="http://foo.com", method="GET")
        self.assertEqual(3, len(self.http_client_mock.method_calls))

    @testing.gen_test
    def test_fetch_500_raises_exc_and_logs_no_password(self):
        # Note: thjis test does not actually validate the logging output. It
        # should, but I don't know how to do that. :)
        e = httpclient.HTTPError(500, "Failure")
        self.http_client_mock.fetch.side_effect = e
        with self.assertRaises(httpclient.HTTPError):
            yield self.client.fetch(
                url="http://foo.com",
                method="GET",
                auth_username="user",
                auth_password="pass",
            )

    @testing.gen_test
    def test_fetch_501_raises_recoverable(self):
        e = httpclient.HTTPError(501, "Failure")
        self.http_client_mock.fetch.side_effect = e
        with self.assertRaises(exceptions.RecoverableFailure):
            yield self.client.fetch(url="http://foo.com", method="GET")


class TestSimpleTokenRestClient(testing.AsyncTestCase):
    def setUp(self, *args, **kwargs):
        super(TestSimpleTokenRestClient, self).setUp()
        self.client = api.SimpleTokenRestClient(tokens={"token": "foobar"})
        self.http_response_mock = mock.MagicMock(name="response")
        self.http_client_mock = mock.MagicMock(name="http_client")
        self.http_client_mock.fetch.return_value = tornado_value(
            self.http_response_mock
        )
        self.client._client = self.http_client_mock

    @testing.gen_test
    def test_fetch_get_with_args(self):
        self.http_response_mock.body = '{"foo": "bar"}'
        ret = yield self.client.fetch(url="http://foo.com", method="GET")
        self.assertEqual({"foo": "bar"}, ret)

        # Dig into the http mock, pull out the request object, and lets make
        # sure our token was in it.
        http_req = self.http_client_mock.mock_calls[0]
        http_req = self.http_client_mock.fetch.call_args[0][0].__dict__
        self.assertEqual(http_req["url"], "http://foo.com?token=foobar")
