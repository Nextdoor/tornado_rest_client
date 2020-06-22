"""Tests for the actors.slack package"""

from tornado import testing

from tornado_rest_client.clients import slack
from tornado_rest_client import exceptions


__author__ = 'Matt Wise <matt@nextdoor.com>'


class TestSlack(testing.AsyncTestCase):

    """Unit tests for the Slack API Client."""

    def test_init_missing_tokeb(self):
        with self.assertRaises(exceptions.InvalidCredentials):
            slack.Slack()

    def test_check_results_with_ok_results(self):
        api = slack.Slack(token='unittest')
        results = {
            "ok": True, "channel": "C03H4GRDF", "ts": "1423092527.000006",
            "message": {
                "text": "Hi, testing!",
                "username": "Kingpin",
                "type": "message",
                "subtype": "bot_message",
                "ts": "1423092527.000006"
            }
        }
        self.assertEqual(True, api.check_results(results))

    def test_check_results_with_invalid_creds(self):
        api = slack.Slack(token='unittest')
        results = {'ok': False, 'error': 'invalid_auth'}
        with self.assertRaises(exceptions.InvalidCredentials):
            api.check_results(results)

    def test_check_results_with_failure_response(self):
        api = slack.Slack(token='unittest')
        results = {'ok': False, 'error': 'something went wrong'}
        with self.assertRaises(slack.Error):
            api.check_results(results)

    def test_check_results_with_unexpected_results(self):
        # Restuls were not even JSON
        api = slack.Slack(token='unittest')
        results = 'got some unexpected result'
        with self.assertRaises(slack.RequestFailure):
            api.check_results(results)

        # Results were JSON, but missing error field
        api = slack.Slack(token='unittest')
        results = {'something': 'strange'}
        with self.assertRaises(slack.RequestFailure):
            api.check_results(results)
