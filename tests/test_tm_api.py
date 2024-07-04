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


def test_id_to_name_list_of_single_uid(napi_instance):
    tekky_uid = "a198e640-779a-47c0-97b5-9d38a351e7fa"
    # test passing a list of uids
    res = napi_instance.trackmania_api.get_account_name([tekky_uid])

    # check result is not empty and only contains one element as requested
    assert len(res) == 1
    # check result contains requested data (UID as key)
    assert res.get(tekky_uid, None) is not None
    # check data is in expected format
    assert isinstance(res[tekky_uid], str)


def test_id_to_name_list_of_multiple_uids(napi_instance):
    tekky_uid = "a198e640-779a-47c0-97b5-9d38a351e7fa"
    eldjinn_uid = "df3ac93d-0c8b-4d92-85d8-cae4afea9413"
    # test passing a list of uids
    res = napi_instance.trackmania_api.get_account_name([tekky_uid, eldjinn_uid])
    print(res)
    # check result is not empty and only contains one element as requested
    assert len(res) == 2
    # check result contains requested data (UID as key)
    assert res.get(tekky_uid, None) is not None and res.get(eldjinn_uid, None) is not None
    # check data is in expected format
    assert isinstance(res[tekky_uid], str)
    assert isinstance(res[eldjinn_uid], str)
