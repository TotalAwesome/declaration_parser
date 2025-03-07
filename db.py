import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    SmallInteger,
    Date,
    or_
)
from sqlalchemy.orm import DeclarativeBase, relationship, Session

from settings import DATE_FORMAT

engine = create_engine("sqlite:///db.sql", echo=True)
session = Session(bind=engine)


class BaseModel(DeclarativeBase):
    pass


class Declaration(BaseModel):

    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment="Дата подачи декларации.")
    applicant = Column(String, nullable=False, comment="Название юр.лица.")
    head_person = Column(String, nullable=True, comment="Руководитель.")
    responsible_person = Column(String, nullable=True, comment="Заявитель.")
    contacts = relationship('Contact', backref='declarations')


class Contact(BaseModel):

    class Type:
        EMAIL = 1
        PHONE = 2
        WEB = 3

    __tablename__ = "contacts"

    value = Column(String, primary_key=True, comment="Контакт")
    contact_type = Column(SmallInteger, nullable=False, comment="Тип контакта")
    declaration_id = Column(Integer, ForeignKey('declarations.id'))


BaseModel.metadata.create_all(bind=engine)


def add_declaration(declaration_id,
                    declaration_date,
                    applicant_name,
                    head_person,
                    responsible_person,
                    *contacts):

    if not contacts:
        return

    query = session.query(Contact).filter(or_(*(Contact.value == contact for contact in contacts)))

    if not session.query(query.exists()).scalar():

        declaration = Declaration(
            id=declaration_id,
            date=datetime.datetime.strptime(declaration_date, DATE_FORMAT).date(),
            applicant=applicant_name,
            head_person=head_person,
            responsible_person=responsible_person
        )

        session.add(declaration)
        session.commit()
        session.refresh(declaration)

        for contact in contacts:
            if '@' in contact:
                contact_type = Contact.Type.EMAIL
            elif '.' in contact:
                contact_type = Contact.Type.WEB
            else:
                contact_type = Contact.Type.PHONE
            session.add(
                Contact(contact_type=contact_type,
                        value=contact,
                        declaration_id=declaration.id)
            )
        session.commit()
    else:
        print("Contacts exists: {}".format(" ".join(contacts)))


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=engine)
    query = session.query(Contact).filter(Contact.value == "hello@mail.ru")
    if not session.query(query.exists()).scalar():
        declaration = Declaration(date=datetime.datetime.now().date(),
                                  applicant="ООО Васильки",
                                  person="Валера Молодец Игоревич")
        session.add(declaration)
        session.commit()
        session.refresh(declaration)
        contact = Contact(contact_type=Contact.Type.EMAIL, value="hello@mail.ru", declaration_id=declaration.id)
        session.add(contact)
        session.commit()
    else:
        pass
