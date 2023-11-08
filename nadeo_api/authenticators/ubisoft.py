from builtins import property
from datetime import datetime

import requests


def valid_ticket(func):
    def check_ticket_valid(self):
        if self._expires and not self._expires < datetime.now():
            return func(self)
        else:
            self._ubisoft_account_login()
            return func(self)
    return check_ticket_valid


class UbisoftAuthenticator:
    def __init__(self, user: str, pwd: str, user_agent: str):
        self._credentials = (user, pwd)
        self.useragent = user_agent
        self._ticket = None
        self._expires = None
        self._sessionId = None
        self._sessionKey = None
        # self._ubisoft_account_login()

    """
    Use of properties to validate valid field contents with decorator
    """
    @property
    @valid_ticket
    def ticket(self):
        return self._ticket

    @property
    @valid_ticket
    def expires(self):
        return self._expires

    @property
    @valid_ticket
    def sessionId(self):
        return self._sessionId

    @property
    @valid_ticket
    def sessionKey(self):
        return self._sessionKey

    def _ubisoft_account_login(self):
        """
        Uses user provided user/password credentials to obtain a
        Ubisoft authentication ticket.

        Returns
        -------
        dict[str, str]:
            Authentication response
        """
        # Setup session to use for Ubisoft Auth and set account credentials
        session = requests.Session()
        session.auth = self._credentials

        # Headers for Ubisoft Auth
        headers = {
            "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
            "Content-Type": "application/json",
            "User-Agent": self.useragent,
        }

        # Post to Ubisoft
        r = session.post(
            "https://public-ubiservices.ubi.com/v3/profiles/sessions",
            headers=headers
        )

        # Check response
        if r.status_code != 200:
            raise ValueError(f"Authentication to Ubisoft Services failed! {r.text}")
        session.close()

        self._ubi_response = r.json()
        self._ticket = self._ubi_response["ticket"]
        self._sessionId = self._ubi_response["sessionId"]
        self._sessionKey = self._ubi_response["sessionKey"]
        # API returns format '2023-10-31T18:22:14.3586538Z'
        # Z signifies UTC
        # fromisoformat only can handle 6 microsecond digits (API return 7)
        self._expires = datetime.fromisoformat(
            self._ubi_response["expiration"][:26].replace("Z", "")
        )