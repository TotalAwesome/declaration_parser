import datetime
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
