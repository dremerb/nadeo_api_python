import json
import pathlib

import pytest

from nadeo_api.authenticators.ubisoft import UbisoftAuthenticator


@pytest.fixture
def account_info():
    with open(pathlib.Path(__file__).parent / "account_info.json") as info:
        acc_info = json.load(info)
    assert acc_info["UBISOFT_LOGIN"]
    assert acc_info["UBISOFT_PASSWORD"]
    assert acc_info["USER_AGENT"]
    yield acc_info


def test_ubisoft_login(account_info):
    print(account_info)
    ubi = UbisoftAuthenticator(
        account_info["UBISOFT_LOGIN"],
        account_info["UBISOFT_PASSWORD"],
        account_info["USER_AGENT"]
    )

    assert ubi.ticket
    assert ubi.sessionId
    assert ubi.sessionKey
    assert ubi.expires
