"""Integration tests for the tornado_rest_client.api module"""

from tornado import httpclient, testing

from tornado_rest_client import api, exceptions


class HTTPBinRestConsumer(api.RestConsumer):

    CONFIG = {
        "path": "/",
        "http_methods": {"get": {}},
        "attrs": {
            "get": {
                "path": "/get",
                "http_methods": {"get": {}},
            },
            "post": {
                "path": "/post",
                "http_methods": {"post": {}},
            },
            "put": {
                "path": "/put",
                "http_methods": {"put": {}},
            },
            "delete": {
                "path": "/delete",
                "http_methods": {"delete": {}},
            },
            "status": {
                "path": "/status/%res%",
                "http_methods": {"get": {}},
            },
            "basic_auth": {
                "path": "/basic-auth/username/password",
                "http_methods": {"get": {}},
            },
        },
    }
    ENDPOINT = "http://httpbin.org"


class HTTPBinRestConsumerBasicAuthed(HTTPBinRestConsumer):

    CONFIG = dict(HTTPBinRestConsumer.CONFIG).update(
        {
            "auth": {
                "user": "username",
                "pass": "password",
            }
        }
    )


class JSONRestClient(api.RestClient):

    JSON_BODY = True


class IntegrationRestConsumer(testing.AsyncTestCase):

    integration = True

    @testing.gen_test(timeout=60)
    def integration_base_get(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.http_get()
        self.assertIn("DOCTYPE", str(ret))

    @testing.gen_test(timeout=60)
    def integration_get_json(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.get().http_get()
        self.assertEqual(ret["url"], "http://httpbin.org/get")

    @testing.gen_test(timeout=60)
    def integration_get_basic_auth(self):
        httpbin = HTTPBinRestConsumerBasicAuthed()
        ret = yield httpbin.basic_auth().http_get()
        self.assertEqual(ret, {"authenticated": True, "user": "username"})

    @testing.gen_test(timeout=60)
    def integration_get_basic_auth_401(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(exceptions.InvalidCredentials):
            yield httpbin.basic_auth().http_get()

    @testing.gen_test(timeout=60)
    def integration_get_with_args(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.get().http_get(foo="bar", baz="bat")
        self.assertEqual(ret["url"], "http://httpbin.org/get?baz=bat&foo=bar")

    @testing.gen_test(timeout=60)
    def integration_post(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.post().http_post(foo="bar", baz="bat")
        self.assertEqual(ret["url"], "http://httpbin.org/post")
        self.assertEqual(ret["form"], {"foo": "bar", "baz": "bat"})

    @testing.gen_test(timeout=60)
    def integration_post_json(self):
        httpbin = HTTPBinRestConsumer(client=JSONRestClient())
        ret = yield httpbin.post().http_post(foo="bar", baz="bat")
        self.assertEqual(ret["url"], "http://httpbin.org/post")
        self.assertEqual(ret["json"], {"foo": "bar", "baz": "bat"})

    @testing.gen_test(timeout=60)
    def integration_put(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.put().http_put(foo="bar", baz="bat")
        self.assertEqual(ret["url"], "http://httpbin.org/put")
        self.assertEqual(ret["data"], "foo=bar&baz=bat")

    @testing.gen_test(timeout=60)
    def integration_delete(self):
        httpbin = HTTPBinRestConsumer()
        ret = yield httpbin.delete().http_delete(foo="bar", baz="bat")
        self.assertEqual(ret["url"], "http://httpbin.org/delete?baz=bat&foo=bar")

    @testing.gen_test(timeout=60)
    def integration_status_401(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(exceptions.InvalidCredentials):
            yield httpbin.status(res="401").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_403(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(exceptions.InvalidCredentials):
            yield httpbin.status(res="403").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_500(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(httpclient.HTTPError):
            yield httpbin.status(res="500").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_501(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(exceptions.RecoverableFailure):
            yield httpbin.status(res="501").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_502(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(httpclient.HTTPError):
            yield httpbin.status(res="502").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_503(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(httpclient.HTTPError):
            yield httpbin.status(res="503").http_get()

    @testing.gen_test(timeout=60)
    def integration_status_504(self):
        httpbin = HTTPBinRestConsumer()
        with self.assertRaises(httpclient.HTTPError):
            yield httpbin.status(res="504").http_get()
