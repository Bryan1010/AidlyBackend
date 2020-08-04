from models import db
from sqlalchemy import Column, Integer, String, Text


class StartData(db.Model):
    """ StartData Model data class """
    __tablename__ = "StartData"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    mission_statement = Column(Text)
