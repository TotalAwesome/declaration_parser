
def unpack_search_item(item):
    return (
        item["id"],
        item["declDate"],
    )


def unpack_declaration(declaration):
    applicant = declaration["applicant"]
    return (
        applicant["fullName"],
        applicant["surname"],
        applicant["firstName"],
        applicant["patronymic"],
        *[i["value"] for i in applicant["contacts"] if i]
    )