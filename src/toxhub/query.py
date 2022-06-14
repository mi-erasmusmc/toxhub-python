from enum import Enum

from .dataclass import DataClass


class ComparisonOperator(Enum):
    EQUALS = 'EQUALS'
    NOT_EQUAL = 'NOT_EQUAL'
    IN = 'IN'
    LIKE = 'LIKE'
    NOT_IN = 'NOT_IN'
    LESS_THAN = 'LESS_THAN'
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    IS_NULL = 'IS_NULL'
    NOT_NULL = 'NOT_NULL'


class Value:

    def __init__(self, value):
        self.value = value


class Field:

    def __init__(self, data_class_key: DataClass, name: str):
        self.dataClassKey = data_class_key.key()
        self.name = name

    def eq_(self, value):
        return self.__to_field_criteria([Value(value)], ComparisonOperator.EQUALS)

    def not_eq(self, value):
        return self.__to_field_criteria([Value(value)], ComparisonOperator.NOT_EQUAL)

    def in_(self, values: []):
        return self.custom_operator(values, ComparisonOperator.IN)

    def not_in(self, values: []):
        return self.custom_operator(values, ComparisonOperator.NOT_IN)

    def custom_operator(self, values: [], operator: ComparisonOperator):
        vs = list(map(lambda v: Value(v), values))
        return self.__to_field_criteria(vs, operator)

    def __to_field_criteria(self, values: [Value], operator: ComparisonOperator):
        primitive_type = self.__primitive_type()
        fc = FieldCriteria(self, primitive_type, operator, values)
        if primitive_type == 'String':
            fc.caseSensitive = False
        return fc

    def __primitive_type(self) -> str:
        if self.name == 'treatmentRelated':
            return 'Boolean'
        elif ['id', 'compoundId', 'findingId', 'timepoint', 'duration'].__contains__(self.name):
            return 'Integer'
        else:
            return 'String'


class Fields:
    COMPOUND_ID = Field(DataClass.COMPOUND, 'id')
    COMPOUND_NAME = Field(DataClass.COMPOUND, 'name')
    COMPOUND_IDENTIFIER = Field(DataClass.COMPOUND, 'compoundIdentifier')
    COMPOUND_SMILES = Field(DataClass.COMPOUND, 'smiles')
    COMPOUND_ORGANISATION = Field(DataClass.COMPOUND, 'organisation')
    COMPOUND_INCHIKEY = Field(DataClass.COMPOUND, 'inchiKey')

    STUDY_ID = Field(DataClass.STUDY, 'id')
    STUDY_IDENTIFIER = Field(DataClass.STUDY, 'studyIdentifier')
    STUDY_TYPE = Field(DataClass.STUDY, 'studyType')
    STUDY_SPECIES = Field(DataClass.STUDY, 'species')
    STUDY_AGE = Field(DataClass.STUDY, 'age')
    STUDY_STRAIN = Field(DataClass.STUDY, 'strain')
    STUDY_ROUTE = Field(DataClass.STUDY, 'route')
    STUDY_DURATION = Field(DataClass.STUDY, 'duration')
    STUDY_DURATION_UNIT = Field(DataClass.STUDY, 'durationUnit')
    STUDY_PHASE = Field(DataClass.STUDY, 'phase')
    STUDY_CREATED = Field(DataClass.STUDY, 'createdDate')
    STUDY_MODIFIED = Field(DataClass.STUDY, 'modifiedDate')
    STUDY_ORGANISATION = Field(DataClass.STUDY, 'organisation')

    FINDING_ID = Field(DataClass.FINDING, 'id')
    FINDING_IDENTIFIER = Field(DataClass.FINDING, 'findingIdentifier')
    FINDING_NAME = Field(DataClass.FINDING, 'finding')
    FINDING_TYPE = Field(DataClass.FINDING, 'findingType')
    FINDING_CODE = Field(DataClass.FINDING, 'findingCode')
    FINDING_VOCABULARY = Field(DataClass.FINDING, 'findingVocabulary')
    FINDING_SEVERITY = Field(DataClass.FINDING, 'severity')
    FINDING_OBSERVATION = Field(DataClass.FINDING, 'observation')
    FINDING_FREQUENCY = Field(DataClass.FINDING, 'frequency')
    FINDING_DOSE = Field(DataClass.FINDING, 'dose')
    FINDING_TREATMENT_RELATED = Field(DataClass.FINDING, 'treatmentRelated')
    FINDING_COMPOUND_ID = Field(DataClass.FINDING, 'compoundId')
    FINDING_STUDY_ID = Field(DataClass.FINDING, 'studyId')
    FINDING_SEX = Field(DataClass.FINDING, 'sex')
    FINDING_ORGAN = Field(DataClass.FINDING, 'specimenOrgan')
    FINDING_ORGAN_CODE = Field(DataClass.FINDING, 'specimenOrganCode')


class SelectedField:

    def __init__(self, data_class: DataClass):
        self.dataClassKey = data_class.key()
        self.names = data_class.fields()


class SortField:

    def __init__(self, field: Field, order: str = 'ASC'):
        self.field = field
        self.order = order


class FieldCriteria:
    caseSensitive: bool

    def __init__(self, field: Field, primitive_type: str, comparison_operator: ComparisonOperator, values: [Value]):
        self.field = field
        self.primitiveType = primitive_type
        self.comparisonOperator = comparison_operator.value
        self.values = values


class Filter:

    def __init__(self, criteria: [[FieldCriteria]]):
        self.criteria = criteria


class Query:

    def __init__(self, sort_fields: [SortField], filter: Filter, selected_fields: [SelectedField], offset: int = 0,
                 limit: int = 0, result_type: str = 'TREE'):
        self.sortFields = sort_fields
        self.filter = filter
        self.selectedFields = selected_fields
        self.offset = offset
        self.limit = limit
        self.resultType = result_type

    @staticmethod
    def __my_dict(obj):
        if isinstance(obj, list):
            element = []
            for item in obj:
                element.append(Query.__my_dict(item))
            return element
        if not hasattr(obj, "__dict__"):
            return obj
        result = {}
        for key, val in obj.__dict__.items():
            if key.startswith("_"):
                continue
            element = []
            if isinstance(val, list):
                for item in val:
                    element.append(Query.__my_dict(item))
            else:
                element = Query.__my_dict(val)
            result[key] = element
        return result

    def to_dict(self):
        return Query.__my_dict(self)


class QueryBuilder:
    """Construct a simple query to submit to a primitive adaptor"""

    def __init__(self):
        self.dataClasses = []
        self.criteriaList = []

    def select(self, data_class: DataClass):
        """
        :param data_class: Class you wish to select
        :return: QueryBuilder
        """
        self.dataClasses.append(data_class)
        return self

    def select_all(self, data_class: DataClass):
        """
        Select all items available for given DataClass, does not work for findings!

        :param data_class:
        :return:
        """
        if data_class == DataClass.FINDING:
            raise Exception("Don't try and select all findings, this is a bad idea, I won't allow it")
        else:
            return self.select(data_class).where(
                Field(data_class, 'id').custom_operator([-1], ComparisonOperator.NOT_EQUAL))

    def where(self, criteria: FieldCriteria):
        self.criteriaList.append(criteria)
        return self

    def and_(self, criteria: FieldCriteria):
        return self.where(criteria)

    def build(self) -> Query:
        """
        Final method to complete construction of a Query with the QueryBuilder
        :return: A query that can be executed in the primitive adaptor
        """
        sort_field = SortField(Field(self.dataClasses[0], 'id'))
        selected_fields = list(map(lambda dc: SelectedField(dc), self.dataClasses))
        return Query(sort_fields=[sort_field], filter=Filter([self.criteriaList]), selected_fields=selected_fields)
