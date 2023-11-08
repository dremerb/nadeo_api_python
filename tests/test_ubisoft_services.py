import json
import pathlib

import nadeo_api
import pytest

from nadeo_api.ubisoft_services import get_player_profile


@pytest.fixture
def account_info():
    with open(pathlib.Path(__file__).parent / "account_info.json") as info:
        acc_info = json.load(info)
    assert acc_info["UBISOFT_LOGIN"]
    assert acc_info["UBISOFT_PASSWORD"]
    assert acc_info["USER_AGENT"]
    yield acc_info


def test_get_player_profile(account_info):
    nadeo_api.login(
        account_info["UBISOFT_LOGIN"],
        account_info["UBISOFT_PASSWORD"],
        account_info["USER_AGENT"]
    )
    print(nadeo_api.ubisoft_authenticator.ticket)
    ar_down_uid = "8f08302a-f670-463b-9f71-fbfacffb8bd1"
    player_info = get_player_profile(ar_down_uid)
    assert player_info["profiles"] != []
    assert ["profileId", "userId", "platformType", "idOnPlatform",
            "nameOnPlatform"] == list(player_info["profiles"].keys())
    print(player_info)
    assert False
