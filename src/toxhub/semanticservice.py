import json
import urllib.parse

from requests import Response, Session

from .auth import Auth


class SemanticService:

    def __init__(self, url, auth: Auth, client: Session):
        self.url = url + "/api/semanticservice/v1"
        self.__auth = auth
        self.__client = client

    def lookup(self, term: str, vocabularies: [str], n_results: int = 20) -> [str]:
        v = self.__vocabulary_param_string(vocabularies)
        params = {'query': term, 'count': n_results}
        path = "/concept/lookup?" + urllib.parse.urlencode(params) + v
        resp = self.__get(path)
        return resp['terms']

    def normalize(self, term: str, vocabularies: [str] = None, nonpreferred: bool = False) -> []:
        if vocabularies and nonpreferred:
            print("You can't specify a vocabulary and query non-preferred terms, just won't work")
            return []
        if vocabularies is None:
            vocabularies = []
        v = self.__vocabulary_param_string(vocabularies)
        params = {'term': term, 'nonpreferred': nonpreferred}
        path = '/concept/normalize?' + urllib.parse.urlencode(params) + v
        resp = self.__get(path)
        return resp.get('concepts')

    def concept_by_id(self, concept_id: int):
        resp = self.__get(f'/concept/{concept_id}')
        if resp:
            return resp.get('concept')

    def map_to_clinical(self, adverse_event_code: str, organ_code: str) -> []:
        """
        map a preclinical adverse event with organ code to a list of clinical equivalents

        :param adverse_event_code:
        :param organ_code:
        :return: list of mappings
        """
        params = {"adverseEventCode": adverse_event_code, "organCode": organ_code}
        result = self.__get('/concept/map/clinical', params=params)
        if result:
            return result['mappings']

    def map_to_preclinical(self, adverse_event_code: str) -> []:
        """
        map a MedDRA Preferred Term to a list of preclinical organ - finding combinations

        :param adverse_event_code:
        :return: list of mappings
        """
        result = self.__get('/concept/map/preclinical', params={"adverseEventCode": adverse_event_code})
        if result:
            return result['mappings']

    def socs_for_findings(self, findings: [dict]):
        """
        Retrieve the system organ class for a concept code or a MA or PT concept name

        :param findings:
        :return: list of mappings
        """
        if not isinstance(findings, list):
            findings = [findings]

        result = []
        for i in range(0, len(findings), 100):
            codes = self.__keys(findings[i:i + 100])
            if len(codes) > 0:
                socs = self.socs_by_concept_codes(codes)
                result.extend(socs)
        return result

    def socs_by_concept_codes(self, codes: []):
        url = f'{self.url}/concept/map/soc'
        r = self.__client.post(url, headers=self.__auth.header(), json={'conceptCodes': codes})
        return self.__validated(r, url)

    def concept_by_name(self, concept_name: str, vocabularies: [str] = None) -> []:
        if vocabularies is None:
            vocabularies = []
        concepts = self.normalize(concept_name, vocabularies)
        if len(concepts) > 0:
            return concepts
        else:
            return None

    def expand(self, concept_id: int, parent_levels=None, child_levels=None):
        params = {
            'parentlevels': parent_levels if parent_levels else '',
            'childlevels': child_levels if child_levels else ''
        }
        path = f'/concept/{concept_id}/expand?' + urllib.parse.urlencode(params)
        resp = self.__get(path)
        if resp:
            return resp['concepts']

    def __get(self, path: str, params: dict = None):
        url = self.url + path
        if params:
            resp = self.__client.get(url, headers=self.__auth.header(), params=params)
        else:
            resp = self.__client.get(url, headers=self.__auth.header())
        return self.__validated(resp, url)

    @staticmethod
    def __validated(response: Response, url: str):
        if 200 <= response.status_code <= 299:
            return json.loads(response.text)
        elif response.status_code == 404:
            print(f'Request returned 404 {response.text}')
            return None
        elif 400 <= response.status_code <= 499:
            print(f'Something went wrong requesting data from {url} {response.status_code} {response.text}')
        elif 500 <= response.status_code <= 599:
            raise RuntimeError(f'Request to {url} failed: {response.status_code} {response.text}')

    @staticmethod
    def __keys(findings: []):
        if not isinstance(findings, list):
            findings = [findings]

        result = []
        for finding in findings:
            # clinical
            if finding.get('findingVocabulary') == 'MedDRA' and finding.get('findingCode') not in result:
                result.append(finding['findingCode'])
            # preclinical
            elif finding.get('organs') and len(finding.get('organs')) > 0:
                organs = finding.get('organs')
                for o in organs:
                    if o['vocabulary'] == 'MA' and o['code'] not in result:
                        result.append(o['code'])
        return result

    @staticmethod
    def __vocabulary_param_string(vocabularies: [str]):
        string = ''
        for vocabulary in vocabularies:
            string += '&vocabularies=' + vocabulary
        return string
