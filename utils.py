import datetime
import xlsxwriter
from itertools import product
from settings import DATE_FORMAT


class ContactType:
    PHONE = 1
    FAX = 3
    EMAIL = 4
    WEB = 5


def unpack_search_item(item):
    return dict(
        id=item["id"],
        date=datetime.datetime.strptime(item["declDate"], DATE_FORMAT).date(),
        product_group=item["group"],
        product=item["productFullName"],
        applicant=item["applicantName"],
        applicant_address=item["applicantAddress"],
    )


def unpack_declaration(declaration):
    result = {}
    applicant = declaration["applicant"]
    result['head_person'] = " ".join(
        (
            applicant["surname"] or "",
            applicant["firstName"] or "",
            applicant["patronymic"] or "",
            ("({})".format(applicant["headPosition"]) if applicant["headPosition"] else None) or ""
        )
    ).strip() or None
    result['responsible_person'] = " ".join(
        (
            applicant["responsibleSurname"] or "",
            applicant["responsibleFirstName"] or "",
            applicant["responsiblePatronymic"] or "",
            ("({})".format(applicant["responsiblePosition"]) if applicant["responsiblePosition"] else None) or ""
        )
    ).strip() or None

    for contact in applicant["contacts"]:
        keys = {
            ContactType.EMAIL: "email",
            ContactType.WEB: "web",
            ContactType.PHONE: "phone",
            ContactType.FAX: "fax",
        }
        if key := keys.get(contact['idContactType']):
            result[key] = contact['value']
    return result


def save_xlsx(headers=None, data=None, filepath="report.xlsx"):
    if not headers:
        headers = (
            'id',
            'Дата',
            'Предприятие',
            'Руководитель',
            'Заявитель',
            'Группа товоаров',
            'Наименование товоара',
            'Телефон',
            'Факс',
            'Сайт',
            'E-mail'
        )
    workbook = xlsxwriter.Workbook(filepath)
    sheet = workbook.add_worksheet()
    for column, value in enumerate(headers):
        sheet.write(0, column, value)

    sheet.autofilter(0, 0, 0, len(headers))  # Включаем фильтры
    sheet.freeze_panes(1, 1)  # Фиксируем первую строчку с фильтрами

    for row, line in enumerate(data):
        for column, value in enumerate(line):
            sheet.write(row + 1, column, value)
    sheet.autofit(max_width=300)
    workbook.close()
