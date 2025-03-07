import requests
import orjson as json
from utils import *
from copy import deepcopy

from settings import *
from db import add_declaration


class Parser(requests.Session):

    def __init__(self):
        super().__init__()
        self.headers = HEADERS.copy()
        self.authenticate()

    def request(self, *args, **kwargs):
        print(args, kwargs)
        return super().request(*args, **kwargs)

    def authenticate(self):
        response = self.post(url=LOGIN_URL, json=AUTH_PAYLOAD)
        if response.status_code == 200:
            self.headers['authorization'] = response.headers['authorization']

    def get_declaration_page(self, page=0, date=END_DATE):
        url = DECLARATIONS_URL.format("get")
        payload = deepcopy(GET_PAYLOAD)
        payload['filter']['regDate'] = {"minDate": date, "maxDate": date}
        payload['page'] = page
        response = self.post(url=url, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)['items']
        return []

    def get_applicant_details(self, _id):
        url = DECLARATIONS_URL.format(_id)  # noqa
        response = self.get(url)
        if response.status_code == 200:
            return unpack_declaration(json.loads(response.text))

    def get_all_declarations(self):

        def extend_info(declaration):
            declaration_data = declaration + self.get_applicant_details(declaration[0])
            print("Try to add: ", declaration_data)
            add_declaration(*declaration_data)
            return True

        page = 0
        while True:
            declarations = map(unpack_search_item, self.get_declaration_page(page))
            data = tuple(map(extend_info, declarations))
            if len(data) != PAGE_SIZE:
                break
            page += 1
        return


if __name__ == "__main__":
    parser = Parser()
    data = parser.get_all_declarations()
    pass
