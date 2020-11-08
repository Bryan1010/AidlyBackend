from models import db
from models.blacklistTokens import BlacklistToken
from mainapp import MAIN_APP
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime, timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import base64


class User(db.Model):
    """ User Model data class """
    __tablename__ = "Users"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    email = Column(String(150), index=True, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mission_statement = Column(Text)
    phone_number = Column(Text)
    interests = db.relationship('UserInterest', backref='user')
    zip = Column(String(20))

    password = Column(String(250), nullable=False)
    authenticated = Column(Boolean, default=False)
    super_admin = Column(Boolean, default=False)

    company = db.relationship('CompanyUsers', backref='user')

    time_availability = Column(String(20))
    week_availability = Column(String(20))
    # appointments = db.EmbeddedDocumentListField(Appointment)
    date_created = Column(DateTime, default=datetime.now())

    def __init__(self, email, password, phone_number, zip, first_name='', last_name='', mission_statement='', super_admin=False):
        self.email = email
        self.password = generate_password_hash(password).decode('utf8')
        self.first_name = first_name
        self.last_name = last_name
        self.mission_statement = mission_statement
        self.super_admin = super_admin
        self.zip = zip

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(MAIN_APP.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = False
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=365, seconds=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(
                payload,
                MAIN_APP.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return e

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(MAIN_APP.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            print('except')
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, MAIN_APP.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
