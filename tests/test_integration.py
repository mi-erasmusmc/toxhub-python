from src.toxhub.datasource import DataSources
from src.toxhub.query import QueryBuilder, Fields, DataClass
from src.toxhub.toxhub import ToxHub
from tests.credentials import Credentials


def main():
    cred = Credentials()
    toxhub = ToxHub(cred.username, cred.password, cred.env, cred.client_secret)

    edema = toxhub.semanticService.normalize('edema', vocabularies=['MedDRA', 'SNOMED'])
    print(toxhub.semanticService.expand(edema[0]['conceptId']))

    omeprazole = toxhub.chemistryService.compound_by_name('omeprazole')
    print(omeprazole)

    similar_compounds = toxhub.similarityService.get(omeprazole.smiles, DataSources.MEDLINE, n_res=20, cutoff=0.5)
    for c in similar_compounds:
        print(c)

    pa = toxhub.primitiveAdaptor
    sources = [DataSources.MEDLINE, DataSources.FAERS, DataSources.CLINCAL_TRIALS, DataSources.ETOX]
    for source in sources:
        query = QueryBuilder().select(DataClass.STUDY).where(Fields.COMPOUND_SMILES.eq_(omeprazole.smiles)).build()
        studies = pa.execute(query, source)
        print(f'{len(studies)} studies in {source}')

    query = QueryBuilder().select(DataClass.FINDING).where(Fields.COMPOUND_SMILES.eq_(omeprazole.smiles)).build()
    findings = pa.execute(query, DataSources.FAERS)
    socs = toxhub.semanticService.socs_for_findings(findings)


if __name__ == "__main__":
    main()
