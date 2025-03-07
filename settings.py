import datetime

DATE_FORMAT = "%Y-%m-%d"
TODAY = datetime.datetime.now().date()
START_DATE = (TODAY - datetime.timedelta(days=365)).strftime(DATE_FORMAT)
END_DATE = TODAY.strftime(DATE_FORMAT)
END_DATE = (TODAY - datetime.timedelta(days=1)).strftime(DATE_FORMAT)
PRODUCT_ORIGIN = "156"  # Китай
PAGE_SIZE = 100

LOGIN_URL = "https://pub.fsa.gov.ru/login"
DECLARATIONS_URL = "https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{}"

AUTH_PAYLOAD = {"password": "hrgesf7HDR67Bd", "username": "anonymous"}

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
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