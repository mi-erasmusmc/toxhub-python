ToxHub
=====

**Python library to interface with eTransafe ToxHub services**

### Requirements

- Python 3.8 +
- Access to ToxHub (username, password, client-secret)

### Installation

```bash
pip install -i https://test.pypi.org/simple/ toxhub
````

### Services available:

- Chemistry Service
- Primitive Adaptors
- Semantic Service
- Similarity Service

### How to use

You can do stuff like so:

```python
from toxhub.dataclass import DataClass
from toxhub.datasource import DataSources
from toxhub.query import QueryBuilder, Fields, ComparisonOperator
from toxhub.toxhub import ToxHub

# Create an instance of ToxHub
toxhub = ToxHub(username='username', password='password', env='dev', client_secret='a uuid provided by gmv')

# Access the various services available in ToxHub

chemistry_service = toxhub.chemistryService
omeprazole = chemistry_service.compound_by_name('Omeprazole')
print(omeprazole)

similarity_service = toxhub.similarityService
similar_compounds = similarity_service.get(omeprazole.smiles, DataSources.MEDLINE)
for compound in similar_compounds:
    print(compound)

# Build elaborate queries for PAs
pa = toxhub.primitiveAdaptor
finding_query = QueryBuilder().select(DataClass.FINDING).where(
    Fields.COMPOUND_INCHIKEY.eq_(omeprazole.inchikey)).and_(
    Fields.FINDING_TYPE.eq_('Histopathology')).and_(
    Fields.FINDING_DOSE.custom_operator(["0", "0.0"], ComparisonOperator.NOT_IN)).build()
findings = pa.execute(finding_query, DataSources.ETOX)

# Or keep it simple
all_compounds_query = QueryBuilder().select_all(DataClass.COMPOUND).build()
compounds = pa.execute(all_compounds_query, DataSources.PSUR)
```

### Contributions

Contributions and constructive feedback are welcome, please get in touch with Erik or Rowan

