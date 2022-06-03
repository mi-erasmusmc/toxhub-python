import json

from requests import Session

from .auth import Auth
from .datasource import DataSource
from .query import Query, DataClass


class PrimitiveAdaptor:

    def __init__(self, url: str, auth: Auth, client: Session):
        self.url = url
        self.__auth = auth
        self.__client = client

    def execute(self, query: Query, datasource: DataSource, converter=lambda x: x) -> []:
        """
        Execute a query on ToxHub

        :param query: Query to be executed, can easily be constructed with the QueryBuilder
        :param datasource: Data source at which the query is targeted
        :param converter: optional conversion of returned items, for example 'lambda x: Compound(x)'
        :return: list of items
        """
        url = f'{self.url}{datasource.path}/query'
        total = 1
        default_batch_size = 5000
        query_results = []
        fetch_all = query.limit == 0 or query.limit > default_batch_size
        # We will copy the original offset and limit and put it back,
        # so we don't sneakily modify the original query and cause confusion
        original_offset = int(query.offset)
        original_limit = int(query.limit)
        query.limit = default_batch_size if fetch_all else query.limit
        while total > query.offset:
            resp = self.__client.post(url, headers=self.__auth.header(), json=query.to_dict())
            if resp.status_code != 200:
                print(f'Request to {url} failed {resp.status_code} {resp.text}')
                return query_results
            result_data = json.loads(resp.text)['resultData']
            query_results.extend(result_data['data'])
            total = result_data['total']
            query.offset += default_batch_size
            # If default limit was overridden we will not get everything, but stick to user defined limit
            if not fetch_all and len(query_results) >= query.limit:
                break
        # leaving query in same state as we found it
        query.offset = original_offset
        query.limit = original_limit
        return list(map(converter, query_results))

    def compound(self, idx: int, data_source: DataSource):
        return self.__item(idx, data_source, DataClass.COMPOUND)

    def study(self, idx: int, data_source: DataSource):
        return self.__item(idx, data_source, DataClass.STUDY)

    def finding(self, idx: int, data_source: DataSource):
        return self.__item(idx, data_source, DataClass.FINDING)

    def findings(self, ids: [int], data_source: DataSource) -> []:
        url = f'{self.url}{data_source.path}/data/FINDING/batch'
        r = self.__client.post(url, json={'ids': ids}, headers=self.__auth.header())
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            print(f'Failed to load findings from {data_source}')

    def __item(self, idx: int, data_source: DataSource, data_class: DataClass):
        url = f'{self.url}{data_source.path}/data/{data_class.key()}/{idx}'
        r = self.__client.get(url, headers=self.__auth.header())
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            print(f'Failed to get {data_class.key().lower()} {idx} from {data_source}')

    def external_additional_property(self, idx: int, property_name: str, data_class: DataClass,
                                     data_source: DataSource):
        url = f'{self.url}{data_source.path}/data/{data_class.key()}/{idx}/additionalproperties'
        batch_size = 1000
        query = {
            "propertyName": property_name,
            "resultType": "TREE",
            "offset": 0,
            "limit": batch_size
        }
        total = 1
        result = []
        while total > query['offset']:
            r = self.__client.post(url, headers=self.__auth.header(), json=query)
            if r.status_code == 200:
                response = json.loads(r.text)
                result.extend(response['data'])
                total = response['total']
                query['offset'] += batch_size
            else:
                print(f"Cannot retrieve compoundIds from {url}: {r.status_code}")
                break
        return result
