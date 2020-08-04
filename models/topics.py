from models import db
from sqlalchemy import Column, Integer


class Topic(db.Model):
    """ Topic Model data class """
    __tablename__ = "Topics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    users_interested = db.relationship('UserTopic', backref='UserTopic')
    company_interested = db.relationship('CompanyTopic', backref='CompanyTopic')


class UserTopic(db.Model):
    """ User Topic Model data class """
    __tablename__ = "UserTopics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)


class CompanyTopic(db.Model):
    """ Company Topic Model data class """
    __tablename__ = "CompanyTopics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)
