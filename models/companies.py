from models import db
from sqlalchemy import *
from datetime import datetime


class Company(db.Model):
    """ Company Model data class """
    __tablename__ = "Companies"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=false)

    logo_url = Column(Text)

    # Company colors Hex values
    primary_color = Column(String(10))
    secondary_color = Column(String(10))

    ein = Column(String(50))
    mission_statement = Column(Text)

    main_contact = Column(Integer, db.ForeignKey('Users.id'))

    company_type_id = Column(Integer, db.ForeignKey('CompanyTypes.id'))

    addresses = db.relationship('CompanyAddress', backref='company')

    date_created = Column(DateTime, default=datetime.now())

    users = db.relationship('CompanyUsers', backref='company')

    # positions = db.EmbeddedDocumentListField(Position)


class CompanyUsers(db.Model):
    """ Company Users Model data class """
    __tablename__ = "CompanyUsers"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    is_admin = Column(Boolean, default=False)


class CompanyType(db.Model):
    """ Company Type Model data class """
    __tablename__ = "CompanyTypes"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    TypeName = Column(String(100))
    companies = db.relationship('Company', backref='type')


class CompanyAddress(db.Model):
    """ Company Address Model Data class """
    __tablename__ = "CompanyAddresses"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'))
    address1 = Column(String(100))
    address2 = Column(String(100))
    address3 = Column(String(100))
    city = Column(String(100))
    zip = Column(String(20))

    # We need the ISO code for the state
    state = Column(String(2))

    # We need to ISO 2 letter code for Country
    country = Column(String(2))

    is_primary = Column(Boolean)
