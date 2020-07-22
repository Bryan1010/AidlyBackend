from models import db
from sqlalchemy import Column, Integer, String


class Interest(db.Model):
    """ Interest Model data class """
    __tablename__ = "Interests"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    interest_name = Column(String(50))
    users_interested = db.relationship('UserInterest', backref='UserInterest')
    company_interested = db.relationship('CompanyInterest', backref='CompanyInterest')


class UserInterest(db.Model):
    """ User Interest Model data class """
    __tablename__ = "UserInterests"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'))
    interest_id = Column(Integer, db.ForeignKey('Interests.id'))


class CompanyInterest(db.Model):
    """ Company Interest Model data class """
    __tablename__ = "CompanyInterests"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'))
    interest_id = Column(Integer, db.ForeignKey('Interests.id'))
