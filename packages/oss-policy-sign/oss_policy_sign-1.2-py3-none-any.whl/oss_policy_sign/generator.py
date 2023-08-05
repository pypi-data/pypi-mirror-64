import base64
import datetime
import time
import json
import hmac
from hashlib import sha1

from .exceptions import TooShortTimeout


def get_iso_8601(expire):
    expire = int(time.time()) + expire
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    return "{}Z".format(gmt)


class OssPolicyAuth():

    def __init__(self,
                 access_key_id,
                 access_key_secret,
                 timeout=60,
                 max_size=10):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

        # Going to expire in duration seconds
        self.timeout = timeout * 60

        # limit of the max_size of uploading files
        self.max_size = max_size

    def get_policy(self):
        policy_text = {
            "expiration": get_iso_8601(self.timeout),
            "conditions": [
                ['content-length-range', 0, self.max_size * 1024 * 1024]
            ]
        }
        policy = json.dumps(policy_text)
        return base64.b64encode(policy.encode()).strip()

    def get_sign(self):
        policy = self.get_policy()
        h = hmac.new(self.access_key_secret.encode(), policy, sha1)
        return base64.encodebytes(h.digest()).strip()

    def get_token(self):
        timeout = self.timeout - 5 * 60
        if (timeout <= 0):
            raise TooShortTimeout()

        expire_at = get_iso_8601(timeout)

        return {
            "policy": self.get_policy(),
            "signature": self.get_sign(),
            "expire_at": expire_at,
            "access_key": self.access_key_id
        }
