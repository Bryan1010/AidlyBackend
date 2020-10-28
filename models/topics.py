from models import db
from sqlalchemy import Column, Integer, Text, Float


class Topic(db.Model):
    """ Topic Model data class """
    __tablename__ = "Topics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(Text)
    users_interested = db.relationship('UserTopic', backref='UserTopic')
    company_interested = db.relationship('CompanyTopic', backref='CompanyTopic')


class UserTopic(db.Model):
    """ User Topic Model data class """
    __tablename__ = "UserTopics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)
    perc = Column(Float)
    
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

class CompanyTopic(db.Model):
    """ Company Topic Model data class """
    __tablename__ = "CompanyTopics"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)
    topic_id = Column(Integer, db.ForeignKey('Topics.id'), primary_key=True)
    perc = Column(Float)


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