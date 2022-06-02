from src.toxhub.datasource import DataSources
from src.toxhub.toxhub import ToxHub
from tests.credentials import Credentials


def main():
    cred = Credentials()
    toxhub = ToxHub(cred.username, cred.password, cred.env, cred.client_secret)

    spaces = toxhub.similarityService.space_names()
    print(spaces)

    omeprazole = toxhub.chemistryService.compound_by_name('omeprazole').smiles
    similar_compounds = toxhub.similarityService.get(omeprazole, DataSources.MEDLINE, cutoff=0.3)

    for compound in similar_compounds:
        print(compound)


if __name__ == "__main__":
    main()
