from enum import Enum


class DataClass(Enum):
    COMPOUND = ('COMPOUND',
                ['id', 'name', 'compoundIdentifier', 'inchiKey', 'smiles', 'organisation'])
    STUDY = ('STUDY', ['id', 'studyType', 'species', 'age', 'strain', 'route', 'duration', 'durationUnit', 'phase',
                       'modifiedDate', 'createdDate', 'organisation', 'studyIdentifier'])
    FINDING = ('FINDING',
               ['id', 'findingIdentifier', 'organs', 'finding',
                'findingCode', 'findingVocabulary', 'severity', 'observation', 'frequency', 'dose', 'timepoint',
                'treatmentRelated', 'compoundId', 'studyId', 'timepointUnit', 'findingType', 'sex'])

    def key(self) -> str:
        return self.value[0]

    def fields(self) -> [str]:
        return self.value[1]


class Compound:

    def __init__(self, c: dict):
        self.id: int = int(c.get('id'))
        self.name: str = c.get('name')
        self.identifier: str = c.get('compoundIdentifier')
        self.inchikey: str = c.get('inchiKey')
        self.smiles: str = c.get('smiles')
        self.organisation: str = c.get('organisation')
        self.confidentiality: str = c.get('confidentiality')

    def __str__(self):
        return str(self.__dict__)


class Organ:

    def __init__(self, o: dict):
        self.id: int = o.get('id')
        self.name: str = o.get('name')
        self.code: str = o.get('code')
        self.vocabulary: str = o.get('vocabulary')

    def __str__(self):
        return str(self.__dict__)


class Frequency:
    affected: int
    at_risk: int

    def __init__(self, original: str):
        if original:
            self.at_risk = 0
            if '/' in original:
                splits = original.split('/')
                aff = splits[0]
                if aff.isdigit():
                    self.affected = int(splits[0])
                if len(splits) > 1:
                    rsk = splits[1]
                    if rsk.isdigit():
                        self.at_risk = int(splits[1])
            elif original.isdigit():
                self.affected = int(original)

    def __str__(self):
        return str(self.__dict__)


class Finding:

    def __init__(self, f: dict):
        self.id: int = int(f.get('id'))
        self.identifier: str = f.get('findingIdentifier')
        self.name: str = f.get('finding')
        self.code: str = f.get('findingCode')
        self.vocabulary: str = f.get('findingVocabulary')
        self.severity: str = f.get('severity')
        self.observation: str = f.get('observation')
        self.frequency: Frequency = Frequency(f.get('frequency'))
        self.dose: str = f.get('dose')
        self.timePoint: str = f.get('timepoint')
        self.timePointUnit: str = f.get('timepointUnit')
        self.treatmentRelated = f.get('treatmentRelated')
        self.compoundId: int = int(f.get('compoundId'))
        self.studyId: int = int(f.get('studyId'))
        self.type: str = f.get('findingType')
        self.sex: str = f.get('sex')
        self.organs: [Organ] = list(map(lambda o: Organ(o), f.get('organs'))) if f.get('organs') else []

    def __str__(self):
        return str(self.__dict__)


class Study:

    def __init__(self, s: dict):
        self.id: int = s.get('id')
        self.type: str = s.get('studyType')
        self.species: str = s.get('species')
        self.age = s.get('age')
        self.route: str = s.get('route')
        self.duration = s.get('duration')
        self.durationUnit: str = s.get('durationUnit')
        self.modified = s.get('modifiedDate')
        self.created = s.get('createdDate')
        self.organisation: str = s.get('organisation')
        self.confidentiality: str = s.get('confidentiality')

    def __str__(self):
        return str(self.__dict__)
