import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    func,
    select,
    text
)
from sqlalchemy.orm import DeclarativeBase, Session


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


def get_max_date():
    statement = select(func.max(Declaration.date))
    return session.execute(statement).scalar()


def select_for_export(start_date, end_date):
    where_statement = ""
    if start_date and end_date:
        where_statement = f"WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    query = f"""
    SELECT 
        id,
        date,
        applicant,
        head_person,
        responsible_person,
        product_group,
        product,
        phone,
        fax,
        web,
        email
    FROM declarations
    {where_statement}
    ORDER BY date DESC
    """
    return session.execute(text(query)).fetchall()