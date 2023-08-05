from datetime import datetime, timezone, timedelta
from unittest import TestCase
from ..generator import OssPolicyAuth


class TestAuth(TestCase):
    def setUp(self):
        self.oss = OssPolicyAuth(access_key_id="1", access_key_secret="2")

    def test_token(self):
        token = self.oss.get_token()
        expire_at_string = token["expire_at"]
        expire_at = datetime.strptime(expire_at_string,
                                      "%Y-%m-%dT%H:%M:%S%z")
        self.assertLess(expire_at - datetime.now(timezone.utc),
                        timedelta(self.oss.timeout))

        self.assertTrue(token["policy"])
        self.assertTrue(token["signature"])
