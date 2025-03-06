import requests
import orjson as json
from utils import *
from copy import deepcopy

from settings import *


class Parser(requests.Session):

    def __init__(self):
        super().__init__()
        self.headers = HEADERS
        self.authenticate()

    def request(self, *args, **kwargs):
        # print(args, kwargs)
        return super().request(*args, **kwargs)

    def authenticate(self):
        payload = {"password": "hrgesf7HDR67Bd", "username": "anonymous"}
        response = self.post(url="https://pub.fsa.gov.ru/login", json=payload)
        if response.status_code == 200:
            self.headers['authorization'] = response.headers['authorization']

    def get_declaration_page(self, page=0):
        url = "https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get"
        payload = deepcopy(GET_PAYLOAD)
        payload['filter']['regDate'] = {"minDate": START_DATE, "maxDate": END_DATE}
        payload['page'] = page
        response = self.post(url=url, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)['items']
        return []

    def get_applicant_details(self, _id):
        url = f"https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{_id}"  # noqa
        response = self.get(url)
        if response.status_code == 200:
            return unpack_declaration(json.loads(response.text))

    def get_all_declarations(self):
        page = 0
        result = []
        while True:
            if data := self.get_declaration_page(page):
                data = tuple(map(lambda x: x + self.get_applicant_details(x[0]),
                             map(unpack_search_item, data)))
                result.extend(data)
                page += 1
            if len(data) != PAGE_SIZE:
                break
        return result


if __name__ == "__main__":
    parser = Parser()
    data = parser.get_all_declarations()
    pass
