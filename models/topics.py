from models import db
from sqlalchemy import Column, Integer


class Topic(db.Model):
    """ Matches Model data class """
    __tablename__ = "Topics"
    id = Column(Integer, index=True, primary_key=True)
    users_topics = db.relationship('UserTopic', backref='UserTopic')
    company_topics = db.relationship('CompanyTopic', backref='CompanyTopic')


class UserTopic(db.Model):
    """ Matches Model data class """
    __tablename__ = "UserTopic"
    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)


class CompanyTopic(db.Model):
    """ Matches Model data class """
    __tablename__ = "CompanyTopic"
    id = Column(Integer, index=True, primary_key=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)