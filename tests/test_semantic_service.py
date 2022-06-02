from src.toxhub.toxhub import ToxHub
from tests.credentials import Credentials


def main():
    # Authentication
    cred = Credentials()
    toxhub = ToxHub(cred.username, cred.password, cred.env, cred.client_secret)

    semantic_service = toxhub.semanticService

    lookup = semantic_service.lookup('inflammatio', ['HPATH'])
    print(lookup)

    by_name = semantic_service.concept_by_name('inflammation')
    print(by_name)

    normalize = semantic_service.normalize('lung', ['MA'])
    print(normalize)

    by_id = semantic_service.concept_by_id(70000414)
    print(by_id)

    map_to_clin = semantic_service.map_to_clinical('MC:0000010', 'MA:0000415')
    print(map_to_clin)

    map_to_preclin = semantic_service.map_to_preclinical('10003441')
    print(map_to_preclin)

    socs = semantic_service.socs_by_concept_codes(['10003441'])
    print(socs)

    expand = semantic_service.expand(36211227, parent_levels=1)
    print(expand)


if __name__ == "__main__":
    main()
