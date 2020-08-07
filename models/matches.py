from models import db
from sqlalchemy import Column, Integer, Text

class Matches(db.Model):
    """ Matches Model data class """
    __tablename__ = "Matches"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('Users.id'), primary_key=True)
    company_id = Column(Integer, db.ForeignKey('Companies.id'), primary_key=True)