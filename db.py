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

engine = create_engine("sqlite:///db.sql", echo=False)
session = Session(bind=engine)


class BaseModel(DeclarativeBase):
    pass


class Declaration(BaseModel):

    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment="Дата подачи декларации")
    applicant = Column(String, nullable=False, comment="Название юр.лица")
    applicant_address = Column(String, nullable=True, comment="Адрес")
    head_person = Column(String, nullable=True, comment="Руководитель")
    responsible_person = Column(String, nullable=True, comment="Заявитель.")
    product_group = Column(String, nullable=True, comment="Общее наименование продукции")
    product = Column(String, nullable=True, comment="Наименование продукта")
    phone = Column(String, nullable=True, comment="Телефон")
    fax = Column(String, nullable=True, comment="Факс")
    web = Column(String, nullable=True, comment="Сайт")
    email = Column(String, nullable=True, comment="Е-почта")


BaseModel.metadata.create_all(bind=engine)


def declaration_not_exists(declaration_id):
    query = session.query(Declaration).filter(Declaration.id == declaration_id)
    return not session.query(query.exists()).scalar()


def add_declaration(**kwargs):
    declaration = Declaration(**kwargs)
    session.add(declaration)
    session.commit()

