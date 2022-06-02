import requests

from .auth import Auth
from .chemistryservice import ChemistryService
from .primitiveadaptor import PrimitiveAdaptor
from .semanticservice import SemanticService
from .similarityservice import SimilarityService


class ToxHub:

    def __init__(self, username: str, password: str, env: str, client_secret: str):
        print('Initializing ToxHub')
        auth = Auth(username, password, env, client_secret)
        url = f'https://{env}.toxhub.etransafe.eu'
        session = requests.Session()
        self.auth = auth
        self.semanticService = SemanticService(url, auth, session)
        self.chemistryService = ChemistryService(url, auth, session)
        self.similarityService = SimilarityService(url, auth, session)
        self.primitiveAdaptor = PrimitiveAdaptor(url, auth, session)
        print('Initialized ToxHub')
