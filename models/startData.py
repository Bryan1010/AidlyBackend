from models import db
from sqlalchemy import Column, Integer, String, Text, false


class StartData(db.Model):
    """ StartData Model data class """
    __tablename__ = "StartData"
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=false)
    mission_statement = Column(Text)
