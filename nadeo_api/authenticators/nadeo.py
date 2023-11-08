import base64
import json
from datetime import datetime

import requests

AUDIENCES = ["NadeoServices", "NadeoLiveServices", "NadeoClubServices"]


def valid_token(func):
    def check_token_valid(self):
        # check if timestamp for earliest refresh is set.
        # check if current datetime is between earliest refresh date and expiration
        # -> trigger token refresh
        if self._token_refresh_ts < datetime.now().timestamp() < self._token_expires:
            self._token_refresh()
            return func(self)
        # all tokens expired, log in "for the first time"
        elif datetime.now().timestamp() < self._token_expires:
            self._service_login_initial()
            return func(self)
        # else all tokens still valid
        else:
            return func(self)

    return check_token_valid


def token_expiration_extractor(token):
    payload = json.loads(
        base64.urlsafe_b64decode(
            token.split(".")[1]
            + "=" * (4 - len(token.split(".")[1]) % 4)
        )
    )
    # timestamp for expiration, timestamp for earliest renewal
    return payload["exp"], payload["rat"]


class NadeoAuthenticator:
    def __init__(self, ubisoft_authenticator, audience):
        if audience not in AUDIENCES:
            raise ValueError("Invalid Audience")
        self._ubisoft_authenticator = ubisoft_authenticator
        self._audience = audience
        self._access_token = None
        self._token_expires = None
        self._refresh_token = None
        self._token_refresh_ts = None
        self._api_response = None
        self._service_login_initial()

    """
    Use of properties to validate valid field contents with decorator
    """
    @property
    @valid_token
    def access_token(self):
        return self._access_token

    @property
    @valid_token
    def refresh_token(self):
        return self._refresh_token

    @property
    @valid_token
    def token_expires(self):
        return self._token_expires

    @property
    @valid_token
    def token_refresh_ts(self):
        return self._token_refresh_ts

    def _service_login_initial(self):
        session = requests.Session()
        body = {"audience": self._audience}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"ubi_v1 t={self._ubisoft_authenticator.ticket}"
        }

        request_result = session.post(
            "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices",
            json=body,
            headers=headers
        )
        if request_result.status_code != 200:
            raise ValueError(
                f"Authentication to Nadeo (Audience {self._audience}) failed! {request_result.text}"
            )
        self._api_response = request_result.json()
        self._access_token = self._api_response["accessToken"]
        self._token_expires, self._token_refresh_ts = token_expiration_extractor(self._access_token)
        self._refresh_token = self._api_response["refreshToken"]

        session.close()

    def _services_login_refresh(self):
        body = json.dumps({"audience": self._audience})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"nadeo_v1 t={self._refresh_token}",
        }
        request_result = requests.post(
            "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh",
            data=body,
            headers=headers
        )
        if request_result.status_code != 200:
            raise ValueError(f"Refresh of '{self._audience}' token failed!")
        self._api_response = request_result.json()
        self._access_token = self._api_response["accessToken"]
        self._token_expires = token_expiration_extractor(self._access_token)
        self._refresh_token = self._api_response["refreshToken"]
        self._token_refresh_ts = token_expiration_extractor(self._refresh_token)
