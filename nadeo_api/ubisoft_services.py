from typing import Union, Tuple, Dict, Any, TYPE_CHECKING

import requests


class UbisoftServices:
    def __init__(self, ubisoft_authenticator: "UbisoftAuthenticator", user_agent: str):
        self._ubisoft_authenticator = ubisoft_authenticator
        self._user_agent = user_agent

    def _request_executor(self, url: str) -> Dict[str, Any]:
        if not self._ubisoft_authenticator:
            raise RuntimeError("Not logged in! Please call the module's login() method first!")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self._user_agent,
            "Authorization": f"ubi_v1 t={self._ubisoft_authenticator.ticket}",
            "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
            "Ubi-SessionId": self._ubisoft_authenticator.sessionId,
        }
        result = requests.get(url, headers=headers)
        return result.json()

    def get_player_profile(self, player_uids: Union[str, Tuple[str]]):
        url = "https://public-ubiservices.ubi.com/v3/profiles?profileIds="
        if isinstance(player_uids, tuple):
            url += ",".join(player_uids)
        else:
            url += player_uids
        return self._request_executor(url)
