import argparse
import requests
import orjson as json
import time

from utils import *
from copy import deepcopy

from settings import *
from db import add_declaration, declaration_not_exists, get_max_date, select_for_export


class Parser(requests.Session):

    def __init__(self):
        super().__init__()
        self.headers = HEADERS.copy()
        self.authenticate()

    def request(self, *args, **kwargs):
        print(args, kwargs)
        while True:
            err = None
            try:
                response = super().request(*args, **kwargs)
            except Exception as exc:
                err = True
                print(exc)
            if err or response.status_code >= 500:
                print('Retry: ', args, kwargs)
                time.sleep(3)
                continue
            elif response.status_code == 401:
                self.authenticate()
            else:
                return response

    def authenticate(self):
        response = self.post(url=LOGIN_URL, json=AUTH_PAYLOAD)
        if response.status_code == 200:
            self.headers['authorization'] = response.headers['authorization']

    def get_declaration_page(self, page=0, date=END_DATE):
        url = DECLARATIONS_URL.format("get")
        payload = deepcopy(GET_PAYLOAD)
        payload['filter']['regDate'] = {"minDate": START_DATE, "maxDate": END_DATE}
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
        else:
            raise Exception(f"{response.status_code}: {response.text}")

    def get_all_declarations(self):

        def extend_info(declaration):
            if declaration_not_exists(declaration['id']):
                declaration_data = declaration | self.get_applicant_details(declaration['id'])
                print("Try to add: ", declaration_data)
                add_declaration(**declaration_data)
            else:
                print("Declaration exists: ", declaration['id'])

        page = 0
        while True:
            declarations = map(unpack_search_item, self.get_declaration_page(page))
            data = tuple(map(extend_info, declarations))
            if len(data) != PAGE_SIZE:
                break
            page += 1
            time.sleep(2)
        return


def parse_data(args):
    if args.start_date:
        globals()['START_DATE'] = args.start_date
    elif max_date := get_max_date():
        globals()['START_DATE'] = max_date.strftime(DATE_FORMAT)
    if args.end_date:
        globals()['END_DATE'] = args.end_date

    parser = Parser()
    parser.get_all_declarations()


def export_xls(args):
    data = select_for_export(start_date=args.start_date, end_date=args.end_date)
    save_xlsx(data=data)
    pass


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Парсер деклараций.", add_help=False)
    commands = arg_parser.add_subparsers()

    parse = commands.add_parser('parse', help='Произвести сбор данных.')
    parse.add_argument('-s', '--start_date', action='store', help='Начало периода для сбора. Пример: 2024-06-25')
    parse.add_argument('-e', '--end_date', action='store', help='Конец периода для сбора. Пример: 2024-06-25')
    parse.set_defaults(func=parse_data)

    export = commands.add_parser('export', help='Произвести выгрузку данных.')
    export.add_argument('-s', '--start_date', action='store', help='Начало периода для сбора. Пример: 2024-06-25')
    export.add_argument('-e', '--end_date', action='store', help='Конец периода для сбора. Пример: 2024-06-25')
    export.set_defaults(func=export_xls)

    args = arg_parser.parse_args()
    args.func(args)

    # parser = Parser()
    # data = parser.get_all_declarations()
    # pass
