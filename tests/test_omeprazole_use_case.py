import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.toxhub.dataclass import DataClass
from src.toxhub.datasource import DataSources
from src.toxhub.primitiveadaptor import PrimitiveAdaptor
from src.toxhub.query import QueryBuilder, Fields, ComparisonOperator
from src.toxhub.toxhub import ToxHub
from tests.credentials import Credentials


def etox_findings(inchikey: str, pa: PrimitiveAdaptor):
    q = QueryBuilder().select(DataClass.FINDING).where(Fields.COMPOUND_INCHIKEY.eq_(inchikey)).and_(
        Fields.FINDING_TYPE.eq_('Histopathology')).and_(
        Fields.FINDING_DOSE.custom_operator(["0"], ComparisonOperator.NOT_IN)).build()
    return pa.execute(q, DataSources.ETOX)


def main():
    # Authentication
    cred = Credentials()
    toxhub = ToxHub(cred.username, cred.password, cred.env, cred.client_secret)

    # Compound name to standard name and structure using chemistry service
    chem_serv = toxhub.chemistryService
    omeprazole = chem_serv.compound_by_name('Omeprazole')
    print(omeprazole)

    # Similar compounds from similarity service
    simil_serv = toxhub.similarityService
    sim_compounds = simil_serv.get(omeprazole.smiles, DataSources.MEDLINE)
    for compound in sim_compounds:
        print(compound)

    # Standardize compounds to get inchikeys which will be used to search databases
    standardized_compounds = list(map(lambda c: chem_serv.compound_by_name(c.name), sim_compounds))
    for compound in standardized_compounds:
        print(f'{compound.name} {compound.inchikey}')

    # Get all findings for each compound from various data sources
    pa = toxhub.primitiveAdaptor
    data_sources = [DataSources.ETOX, DataSources.MEDLINE, DataSources.FAERS, DataSources.CLINCAL_TRIALS,
                    DataSources.DAILYMED]
    for source in data_sources:
        compound_soc_count_list = []
        for compound in standardized_compounds:
            # Get all the findings for inchikey
            query = QueryBuilder().select(DataClass.FINDING).where(
                Fields.COMPOUND_INCHIKEY.eq_(compound.inchikey)).build()
            findings = etox_findings(compound.inchikey, pa) if source.path == DataSources.ETOX.path else pa.execute(
                query, source)
            print(f'{len(findings)} findings for {compound.name} in {source}')

            # Translate findings to socs
            socs_map = toxhub.semanticService.socs_for_findings(findings)
            socs = []
            for f in socs_map:
                mappings = f['mapping']
                for mapping in mappings:
                    socs.append(str(mapping['conceptName'])[0:25])
            # Count occurrences for each soc
            for soc_name in set(socs):
                compound_soc_count_list.append(
                    {'compound': compound.name, 'soc': soc_name, 'count': int(socs.count(soc_name))})

        # Put the list in a data frame and show the heatmap
        df = pd.DataFrame(compound_soc_count_list)
        f, ax = plt.subplots()
        ax.set_title(source.__str__())
        ax = sns.heatmap(df.pivot('soc', 'compound', values='count'), linewidth=1, cmap="YlGnBu", annot=True,
                         fmt=".0f")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
