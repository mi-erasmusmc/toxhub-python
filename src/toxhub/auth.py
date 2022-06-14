import json
from datetime import datetime, timedelta

from requests import Session


class Token:

    def __init__(self, value: str, exp: datetime):
        self.value = value
        self.__exp = exp

    def is_valid(self) -> bool:
        """
        Checks token validity based on expiry time
        :return:
        """
        return self.__exp > datetime.now()


class Auth:
    """Manages authentication with the ToxHub"""

    def __init__(self, username: str, password: str, env: str, client_secret: str, session: Session):
        self.url = f'https://login.{env}.toxhub.etransafe.eu/auth/realms/KH/protocol/openid-connect'
        self.__session = session
        self.__clientSecret = client_secret
        self.__username = username
        self.__password = password
        self.__refresh_token()

    def header(self):
        """
        Get a valid authorization header required for ToxHub services
        :return: Valid authorization header
        """
        return {"Authorization": f"Bearer {self.token()}"}

    def token(self) -> str:
        """
        Get a valid token from ToxHub, only obtains a new token when current token has expired.
        :return: a token
        """
        if not self.__token.is_valid():
            self.__refresh_token()
        return self.__token.value

    def __refresh_token(self):
        data = {'grant_type': 'password', 'username': self.__username, 'password': self.__password,
                'client_id': 'knowledge-hub', 'client_secret': self.__clientSecret}
        r = self.__session.post(f'{self.url}/token', data=data)
        if r.status_code == 200:
            token_value = json.loads(r.text)['access_token']
            token_exp = datetime.now() + timedelta(seconds=int(json.loads(r.text)['expires_in']) - 60)
            self.__token = Token(token_value, token_exp)
            print('Successfully authenticated with ToxHub')
        else:
            print(f'Failed to obtain token, received status code:{r.status_code}')
