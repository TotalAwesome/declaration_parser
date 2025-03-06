
def unpack_search_item(item):
    return (
        item["id"],
        item["declDate"],
    )


def unpack_declaration(declaration):
    applicant = declaration["applicant"]
    person_name = " ".join(
        (
            applicant["surname"] or "",
            applicant["firstName"] or "",
            applicant["patronymic"] or ""
        )
    )
    contacts = (i["value"] for i in applicant["contacts"] if i)
    return (
        applicant["fullName"],
        person_name,
        *contacts
    )
