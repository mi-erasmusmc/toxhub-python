class DataSource:
    """ToxHub Data Source, can be queried with a Primitive Adaptor and has a Chemical Space with similar structures """

    def __init__(self, path: str, chemical_space: str):
        self.path = path
        self.chemicalSpace = chemical_space

    def __str__(self):
        return self.chemicalSpace.replace('pa', '')


class DataSources:
    """Predefined ToxHub data sources"""
    MEDLINE = DataSource('/medlinepa.kh.svc/primitive-adapter/v1', 'medlinepa')
    OFFTARGET = DataSource('/offtargetpa.kh.svc/primitive-adapter/v1', 'offtargetpa')
    FAERS = DataSource('/faerspa.kh.svc/primitive-adapter/v1', 'faerspa')
    CLINCAL_TRIALS = DataSource('/clinicaltrialspa.kh.svc/primitive-adapter/v1', 'clinicaltrialspa')
    DAILYMED = DataSource('/dailymedpa.kh.svc/primitive-adapter/v1', 'dailymedpa')
    ETOX = DataSource('/etoxsyspa.kh.svc/preclinical-platform/api/etoxsys-pa/v1', 'etoxsyspa')
    PRECLINICAL = DataSource('/preclinicaldbpa.kh.svc/preclinical-platform/api/preclinical-db-pa/v1',
                             'preclinicaldbpa')
    PSUR = DataSource('/psurdbpa.kh.svc/primitive-adapter/v1', 'psurdbpa')
