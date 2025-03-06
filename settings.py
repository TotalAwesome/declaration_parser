import datetime

DATE_FORMAT = "%Y-%m-%d"
TODAY = datetime.datetime.now().date()
START_DATE = (TODAY - datetime.timedelta(days=365)).strftime(DATE_FORMAT)
END_DATE = TODAY.strftime(DATE_FORMAT)
PRODUCT_ORIGIN = "156"  # Китай
PAGE_SIZE = 100


HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Origin': 'https://pub.fsa.gov.ru',
    # 'Pragma': 'no-cache',
    # 'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Linux"'
}

GET_PAYLOAD = {
    "size": PAGE_SIZE,
    "page": 0,
    "filter": {
        "status": [],
        "idDeclType": [],
        "idCertObjectType": [],
        "idProductType": [],
        "idGroupRU": [],
        "idGroupEEU": [],
        "idTechReg": [],
        "idApplicantType": [],
        "regDate": {
            "minDate": None,
            "maxDate": None
        },
        "endDate": {
            "minDate": None,
            "maxDate": None
        },
        "columnsSearch": [],
        "number": None,
        "idProductOrigin": [PRODUCT_ORIGIN],
        "idProductEEU": [],
        "idProductRU": [],
        "idDeclScheme": [],
        "awaitOperatorCheck": None,
        "editApp": None,
        "violationSendDate": None,
        "isProtocolInvalid": None,
        "checkerAIResult": None,
        "checkerAIProtocolsResults": None,
        "checkerAIProtocolsMistakes": None,
        "hiddenFromOpen": None
    },
    "columnsSort": [
        {"column": "declDate", "sort": "ASC"}
    ]
}