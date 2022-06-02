import json
import time

from requests import Session

from .auth import Auth
from .datasource import DataSource


class SimilarStructure:

    def __init__(self, name: str, smiles: str, idx: int, distance: float):
        self.name = name
        self.smiles = smiles
        self.id = idx
        self.distance = distance

    def __str__(self):
        return str(self.__dict__)


class SimilarityService:

    def __init__(self, toxhub_url, auth: Auth, client: Session):
        self.__auth = auth
        self.url = toxhub_url + '/flame.kh.svc/api/v1'
        self.__client = client

    def ready(self) -> bool:
        """
        Check readiness of similarity service

        :return: Boolean indiciating whether similarity service is ready or not
        """
        r = self.__client.get(self.url + '/ready', headers=self.__auth.header())
        return r.status_code == 200

    def get(self, smiles, datasource: DataSource, algo: str = 'morganFP', n_res=10, cutoff=0.5) -> [SimilarStructure]:
        """
        Get similar compounds based on smiles available for the provided data source

        :param smiles: smiles to find similiar structures for
        :param datasource: datasource in which to search
        :param algo: e.g. substructureFP, rdkFP, RDKit_md, morganFP
        :param n_res: number of results
        :param cutoff: threshold ranging from 0 - 1
        :return: a list of similar structures
        """
        space = f'{datasource.chemicalSpace}_{algo}'
        url = f'{self.url}/search/space/{space}/version/0/smiles?numsel={n_res}&cutoff={cutoff}'
        r = self.__client.put(url=url, headers=self.__auth.header(), data={'SMILES': smiles})

        result = []

        # get the results from the backend
        if r.status_code == 200:
            search_id = r.text.replace('"', '')
            retry = True
            while retry:
                # Give it one second before trying
                time.sleep(1)
                r2 = self.__client.get(self.url + '/smanage/search/' + search_id, headers=self.__auth.header())
                if r2.status_code == 200:
                    if 'waiting' not in r2.text:
                        obj = json.loads(r2.text)
                        if obj:
                            if ('search_results' in obj) and (len(obj['search_results']) == 1):
                                search_result = obj['search_results'][0]
                                if 'obj_nam' in search_result:
                                    for i in range(len(search_result['obj_nam'])):
                                        result.append(SimilarStructure(
                                            name=search_result['obj_nam'][i],
                                            smiles=search_result['SMILES'][i],
                                            idx=int(search_result['obj_id'][i]),
                                            distance=float('{:.4f}'.format(search_result['distances'][i]))))
                        retry = False
                else:
                    print('Collecting results failed:' + str(r2.status_code) + ', msg:' + r2.text)
                    retry = False
        else:
            print('request failed:' + str(r.status_code) + ', msg:' + r.text)
        return result

    def spaces(self):
        r = self.__client.get(self.url + '/smanage/spaces', headers=self.__auth.header())
        if r.status_code == 200:
            obj = json.loads(r.text)
            return obj[1]

    def space_names(self):
        sps = self.spaces()
        if sps:
            return list(map(lambda s: s['spacename'], sps))
