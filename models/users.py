from models import db
from mainapp import MAIN_APP
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    """ User Model data class """
    __tablename__ = "Users"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    email = Column(String(150), index=True, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mission_statement = Column(Text)
    interests = db.relationship('UserInterest', backref='user')

    password = Column(String(255))
    authenticated = Column(Boolean, default=False)

    company = db.relationship('CompanyUsers', backref='user')

    # time_availability = db.ListField(db.DateTimeField())
    # appointments = db.EmbeddedDocumentListField(Appointment)
    date_created = Column(DateTime, default=datetime.now())

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(MAIN_APP.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(MAIN_APP.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


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
