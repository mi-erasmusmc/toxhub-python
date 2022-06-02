from itertools import groupby

from src.toxhub.dataclass import Compound, Finding
from src.toxhub.datasource import DataSources
from src.toxhub.primitiveadaptor import PrimitiveAdaptor
from src.toxhub.query import QueryBuilder, DataClass, Fields
from src.toxhub.toxhub import ToxHub
from tests.credentials import Credentials


def all_psur_compounds(pa: PrimitiveAdaptor) -> [Compound]:
    q = QueryBuilder().select_all(DataClass.COMPOUND).build()
    return pa.execute(q, DataSources.PSUR, converter=lambda x: Compound(x))


def psur_findings(pa: PrimitiveAdaptor, idx: int) -> [Finding]:
    q = QueryBuilder().select(DataClass.FINDING).where(Fields.FINDING_COMPOUND_ID.eq_(idx)).and_(
        Fields.FINDING_TYPE.in_(['sr_serious_cumulative', 'sr_notserious_cumulative'])).build()
    return pa.execute(q, DataSources.PSUR, converter=lambda x: [str(x['finding']), int(x['frequency'])])


def main():
    cred = Credentials()
    toxhub = ToxHub(cred.username, cred.password, cred.env, cred.client_secret)
    pa = toxhub.primitiveAdaptor

    psur_compounds = all_psur_compounds(pa)
    for compound in psur_compounds:
        print(compound.name)
        all_findings = []
        findings = psur_findings(pa, compound.id)
        for i, g in groupby(sorted(findings), key=lambda x: x[0]):
            all_findings.append([i, sum(v[1] for v in g)])
        for f in all_findings:
            print(f)


if __name__ == "__main__":
    main()
