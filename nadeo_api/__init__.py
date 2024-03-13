from nadeo_api.authenticators.trackmania import TrackmaniaOAuthenticator
from nadeo_api.authenticators.ubisoft import UbisoftAuthenticator
from nadeo_api.nadeo_services import NadeoServices
from nadeo_api.trackmania_api import TrackmaniaAPI
from nadeo_api.ubisoft_services import UbisoftServices
from nadeo_api.nadeo_live_services import NadeoLiveServices


class NadeoAPI:
    def __init__(self, account_mail: str, password: str, user_agent: str, client_id: str, client_secret: str):
        self.ubisoft_authenticator = UbisoftAuthenticator(account_mail, password, user_agent)
        # force login by accessing variable. Raises error on bad credentials
        self.ubisoft_authenticator.ticket
        self.trackmania_authenticator = TrackmaniaOAuthenticator(client_id, client_secret)
        # force login by accessing variable. Raises error on bad credentials
        self.trackmania_authenticator.access_token
        self.ubisoft_services = UbisoftServices(self.ubisoft_authenticator, user_agent)
        self.nadeo_services = NadeoServices(self.ubisoft_authenticator, user_agent)
        self.nadeo_live_services = NadeoLiveServices(self.ubisoft_authenticator, user_agent)
        self.trackmania_api = TrackmaniaAPI(self.trackmania_authenticator, user_agent)