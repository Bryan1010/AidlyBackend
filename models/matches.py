from models import db
from sqlalchemy import Column, Integer, Text, Float

class Matches(db.Model):
    """ Matches Model data class """
    __tablename__ = "Matches"
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)
    user_perc = Column(Float)
    company_perc = Column(Float)
    
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