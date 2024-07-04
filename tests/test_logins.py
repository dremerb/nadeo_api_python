import json
import pathlib

import pytest

from nadeo_api import TrackmaniaOAuthenticator
from nadeo_api.authenticators.ubisoft import UbisoftAuthenticator


@pytest.fixture
def account_info():
    with open(pathlib.Path(__file__).parent / "account_info.json") as info:
        acc_info = json.load(info)
    assert acc_info["UBISOFT_LOGIN"]
    assert acc_info["UBISOFT_PASSWORD"]
    assert acc_info["USER_AGENT"]
    assert acc_info["TM_API_IDENTIFIER"]
    assert acc_info["TM_API_SECRET"]
    yield acc_info


def test_ubisoft_login(account_info):
    print(account_info)
    ubi = UbisoftAuthenticator(
        account_info["UBISOFT_LOGIN"],
        account_info["UBISOFT_PASSWORD"],
        account_info["USER_AGENT"]
    )

    print(ubi.ticket)
    print(ubi.sessionId)
    print(ubi.sessionKey)
    print(ubi.expires)
    assert ubi.ticket
    assert ubi.sessionId
    assert ubi.sessionKey
    assert ubi.expires

def test_trackmania_login(account_info):
    tm = TrackmaniaOAuthenticator(account_info["TM_API_IDENTIFIER"], account_info["TM_API_SECRET"])
    tm._access_token
    assert tm.client_id
    assert tm.client_secret
    assert tm._access_token
    assert tm._token_expires
    assert tm._api_response