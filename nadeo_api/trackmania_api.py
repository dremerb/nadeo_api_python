from typing import Union, List

import requests


class TrackmaniaAPI:
    def __init__(self, authenticator, user_agent: str):
        self._authenticator = authenticator
        self._user_agent = user_agent

    def _request_executor(self, url):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self._user_agent,
            "Authorization": f"Bearer {self._authenticator.access_token}",
        }
        result = requests.get(url, headers=headers)
        return result.json()

    def get_account_name(self, player_uids: Union[str, List[str]]):
        url = "https://api.trackmania.com/api/display-names?accountId[]="
        if isinstance(player_uids, tuple):
            url += ",".join(player_uids)
        else:
            url += player_uids
        return self._request_executor(url)