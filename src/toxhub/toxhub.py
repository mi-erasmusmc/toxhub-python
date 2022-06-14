import requests

from .auth import Auth
from .chemistryservice import ChemistryService
from .primitiveadaptor import PrimitiveAdaptor
from .semanticservice import SemanticService
from .similarityservice import SimilarityService


class ToxHub:

    def __init__(self, username: str, password: str, env: str, client_secret: str, session_verify=True):
        """
        Base class of the ToxHub library

        :param username: Your ToxHub username
        :param password: Your ToxHub password
        :param env: Environment e.g. 'dev', 'test', 'bayer', 'novartis' etc.
        :param client_secret: Each env has its own client secret, contact GMV to find out what it is.
        :param session_verify: Override when using self-signed certificates.
        Set to false if you want to ignore certificate checks,
        alternatively pass path to .pem file to allow self-signed certificate.
        """
        print('Initializing ToxHub')
        url = f'https://{env}.toxhub.etransafe.eu'
        session = requests.Session()
        session.verify = session_verify
        auth = Auth(username, password, env, client_secret, session)
        self.auth = auth
        self.semanticService = SemanticService(url, auth, session)
        self.chemistryService = ChemistryService(url, auth, session)
        self.similarityService = SimilarityService(url, auth, session)
        self.primitiveAdaptor = PrimitiveAdaptor(url, auth, session)
        print('Initialized ToxHub')
