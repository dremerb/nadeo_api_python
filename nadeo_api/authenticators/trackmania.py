import base64
import json
from datetime import datetime, timedelta

import requests

AUDIENCES = ["NadeoServices", "NadeoLiveServices", "NadeoClubServices"]


def valid_token(func):
    def check_token_valid(self):
        # check if timestamp for earliest refresh and expiration are set.
        # check if current datetime is between earliest refresh date and expiration
        # -> trigger token refresh
        if self._token_expires:
            self._services_login()
            return func(self)
        # all tokens expired, log in
        elif datetime.now() < self._token_expires:
            self._service_login()
            return func(self)
        # else all tokens still valid
        else:
            return func(self)

    return check_token_valid


class TrackmaniaOAuthenticator:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = None
        self._token_expires = None
        self._api_response = None
        self._services_login()

    """
    Use of properties to validate valid field contents with decorator
    """
    @property
    @valid_token
    def access_token(self):
        return self._access_token

    @property
    @valid_token
    def token_expires(self):
        return self._token_expires

    def _services_login(self):
        authorization = base64.b64encode(bytes(self.client_id + ":" + self.client_secret, "ISO-8859-1")).decode("ascii")
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        request_result = requests.post(
            "https://api.trackmania.com/api/access_token",
            data=body
        )
        if request_result.status_code != 200:
            raise ValueError(f"Updating Trackmania OAuth token failed!")
        self._api_response = request_result.json()
        self._access_token = self._api_response["access_token"]
        self._token_expires = datetime.now() + timedelta(seconds=self._api_response["expires_in"])
