
def unpack_search_item(item):
    return (
        item["id"],
        item["declDate"],
    )


def unpack_declaration(declaration):
    applicant = declaration["applicant"]
    head_person = " ".join(
        (
            applicant["surname"] or "",
            applicant["firstName"] or "",
            applicant["patronymic"] or "",
            ("({})".format(applicant["headPosition"]) if applicant["headPosition"] else None) or ""
        )
    ).strip() or None
    responsible_person = " ".join(
        (
            applicant["responsibleSurname"] or "",
            applicant["responsibleFirstName"] or "",
            applicant["responsiblePatronymic"] or "",
            ("({})".format(applicant["responsiblePosition"]) if applicant["responsiblePosition"] else None) or ""
        )
    ).strip() or None
    contacts = (i["value"].lower() for i in applicant["contacts"] if i)
    return (
        applicant["fullName"] or head_person or responsible_person,
        head_person,
        responsible_person,
        *set(contacts)
    )
