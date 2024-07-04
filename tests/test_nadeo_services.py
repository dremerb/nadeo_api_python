import json
import pathlib

import pytest

from nadeo_api import NadeoAPI


@pytest.fixture
def napi_instance():
    with open(pathlib.Path(__file__).parent / "account_info.json") as info:
        acc_info = json.load(info)
    assert acc_info["UBISOFT_LOGIN"]
    assert acc_info["UBISOFT_PASSWORD"]
    assert acc_info["USER_AGENT"]
    assert acc_info["TM_API_IDENTIFIER"]
    assert acc_info["TM_API_SECRET"]
    napi = NadeoAPI(
        acc_info["UBISOFT_LOGIN"],
        acc_info["UBISOFT_PASSWORD"],
        acc_info["USER_AGENT"],
        acc_info["TM_API_IDENTIFIER"],
        acc_info["TM_API_SECRET"]
    )
    yield napi

def test_account_webidentities(napi_instance):
    tekky_uid = "a198e640-779a-47c0-97b5-9d38a351e7fa"
    tekky = napi_instance.nadeo_services.get_account_webidentities((tekky_uid,))
    # check result is list
    assert isinstance(tekky, list)
    # check result not empty
    assert len(tekky) >= 1
    # check result is list of dicts
    assert all([isinstance(a, dict) for a in tekky])

    # check expected keys are present in result
    assert all([a["accountId"] == tekky_uid for a in tekky])
    assert all(["provider" in a.keys() for a in tekky])
    assert all(["timestamp" in a.keys() for a in tekky])
    assert all(["uid" in a.keys() for a in tekky])
