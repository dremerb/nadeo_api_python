from typing import Tuple

import requests

from nadeo_api.authenticators.nadeo import NadeoAuthenticator


class NadeoServices(NadeoAuthenticator):
    def __init__(self, ubisoft_authenticator, user_agent: str):
        self._ubisoft_authenticator = ubisoft_authenticator
        self._user_agent = user_agent

    def _request_executor(self, url):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self._user_agent,
            "Authorization": f"nadeo_v1 t={self.access_token}",
        }
        result = requests.get(url, headers=headers)
        return result.json()

    def get_account_display_name(self, account_id: str):
        url = f"https://prod.trackmania.core.nadeo.online/accounts/displayNames/?accountIdList={account_id}"
        return self._request_executor(url)

    def get_account_webidentities(self, account_ids: Tuple[str], merge_results: bool = False, return_dict: bool = False):
        url = f"https://prod.trackmania.core.nadeo.online/webidentities/?accountIdList={','.join(account_ids)}"
        if merge_results or return_dict:
            query_results = self._request_executor(url)
            results = {}
            for qr in query_results:
                # use accountId as temporary keys for merging
                cur_user_data = results.get(qr["accountId"], {"accountId": qr["accountId"], "timestamp": qr["timestamp"]})
                # write uid of `ubiServices`/`uplay` provider as dedicated key
                if qr["provider"] == "ubiServices":
                    cur_user_data["ubiServices_uid"] = qr["uid"]
                elif qr["provider"] == "uplay":
                    cur_user_data["uplay_uid"] = qr["uid"]
                results[qr["accountId"]] = cur_user_data
            if return_dict:
                return results
            # only return values (omit keys)
            return list(results.values())
        return self._request_executor(url)