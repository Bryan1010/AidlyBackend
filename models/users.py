from models import db
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime


class User(db.Model):
    """ User Model data class """
    __tablename__ = "Users"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    email = Column(String(150), index=True, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mission_statement = Column(Text)
    interests = db.relationship('UserInterest', backref='user')

    company_owner = db.relationship('Company', backref='main_contact')

    password = Column(Text)

    # time_availability = db.ListField(db.DateTimeField())

    # appointments = db.EmbeddedDocumentListField(Appointment)
    date_created = Column(DateTime, default=datetime.now())

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Interest(db.Model):
    """ Interest Model data class """
    __tablename__ = "Interests"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    interest_name = Column(String(50))
    users_interested = db.relationship('UserInterest', backref='interest')


class UserInterest(db.Model):
    """ User Interest Model data class """
    __tablename__ = "UserInterests"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    interest_id = Column(Integer, db.ForeignKey('Interests.id'), primary_key=True)
