class DataSource:
    """ToxHub Data Source, can be queried with a Primitive Adaptor and has a Chemical Space with similar structures """

    def __init__(self, path: str, chemical_space: str):
        self.path = path
        self.chemicalSpace = chemical_space

    def __str__(self):
        return self.chemicalSpace.replace('pa', '')

    def __eq__(self, other):
        return other.path == self.path


class DataSources:
    """Predefined ToxHub data sources"""
    CHEMBL = DataSource('/chemblpa.kh.svc/primitive-adapter/v1', 'chemblpa')
    CLINCAL_TRIALS = DataSource('/clinicaltrialspa.kh.svc/primitive-adapter/v1', 'clinicaltrialspa')
    DAILYMED = DataSource('/dailymedpa.kh.svc/primitive-adapter/v1', 'dailymedpa')
    DILIRANK = DataSource('/dilirankpa.kh.svc/primitive-adapter/v1', 'dilirankpa')
    ETOX = DataSource('/etoxsyspa.kh.svc/preclinical-platform/api/etoxsys-pa/v1', 'etoxsyspa')
    FAERS = DataSource('/faerspa.kh.svc/primitive-adapter/v1', 'faerspa')
    MEDLINE = DataSource('/medlinepa.kh.svc/primitive-adapter/v1', 'medlinepa')
    OFFTARGET = DataSource('/offtargetpa.kh.svc/primitive-adapter/v1', 'offtargetpa')
    PRECLINICAL = DataSource('/preclinicaldbpa.kh.svc/preclinical-platform/api/preclinical-db-pa/v1',
                             'preclinicaldbpa')
    PSUR = DataSource('/psurdbpa.kh.svc/primitive-adapter/v1', 'psurdbpa')
    WITHDRAWN_DRUGS = DataSource('/withdrawndrugspa.kh.svc/primitive-adapter/v1', 'withdrawndrugspa')
