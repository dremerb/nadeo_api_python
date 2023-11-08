from nadeo_api.authenticators.ubisoft import UbisoftAuthenticator
from nadeo_api.ubisoft_services import UbisoftServices
from nadeo_api.nadeo_live_services import NadeoLiveServices


class NadeoAPI:
    def __init__(self, account_mail: str, password: str, user_agent: str):
        self.ubisoft_authenticator = UbisoftAuthenticator(account_mail, password, user_agent)
        # force login by accessing variable. Raises error on bad credentials
        self.ubisoft_authenticator.ticket
        self.ubisoft_services = UbisoftServices(self.ubisoft_authenticator, user_agent)
        self.nadeo_live_services = NadeoLiveServices(self.ubisoft_authenticator, user_agent)
