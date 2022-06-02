from requests import Session

from .auth import Auth


class Compound:
    """Standardized compound as returned by Chemistry Service"""

    def __init__(self, compound: dict):
        self.name = compound.get('name')
        self.inchikey = compound.get('inchikey')
        self.smiles = compound.get('smiles')
        self.connectivity = compound.get('connectivity')

    def __str__(self):
        return str(self.__dict__)


class ChemistryService:
    """Provides access to the ToxHub Chemistry Service"""

    def __init__(self, base: str, auth: Auth, client: Session):
        self.__auth = auth
        self.url = base + "/chemistryservice.kh.svc/v1"
        self.__client = client

    def compound_by_name(self, name):
        """Returns a standardized compound object from the chemistry service based on the provided name.
        If name could not be standardized by the chemistry service None is returned"""
        return self.__standardize(name, 'clinical')

    def compound_by_smiles(self, smiles):
        """Returns a standardized compound object from the chemistry service based on the provided smiles.
        If smiles could not be standardized by the chemistry service None is returned"""
        return self.__standardize(smiles, 'preclinical')

    def standardize_smiles(self, smiles):
        """Returns a standardized smiles from the chemistry service based on the provided smiles.
        If smiles could not be standardized by the chemistry service None is returned"""
        compound = self.compound_by_smiles(smiles)
        if compound:
            return compound.smiles
        return None

    def __standardize(self, compound, pa_type):
        """
        Single endpoint provided by Chemistry Service to standardise molecules and retrieve structures from names.
        Compound should be either a name (such as paracetamol) when pa_type is 'clinical',
        or a SMILES string when pa_type is 'clinical'

        :param compound: Either a name or a smiles
        :param pa_type: 'clinical' or 'preclincical'
        :return: Standardized compound object or None
        """
        url = f'{self.url}/pa_standardize'
        r = self.__client.post(url, data={'compound': compound, 'pa_type': pa_type}, headers=self.__auth.header())
        if r.status_code == 200:
            response = r.json()
            if 'Empty response' in response:
                return None
            if 'result' in response:
                c = response['result'][0]
                return Compound(c)
        else:
            print(f"Cannot retrieve compounds from {url}: {r.status_code}")
            print(r.text)
            return None
