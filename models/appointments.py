from models import db
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
import datetime

class Appointment(db.Model):
    """ Appointment class relating back to user """
    user_id = db.ObjectIdField(required=True)
    company_id = db.ObjectIdField(required=True)
    start_date = db.DateTimeField(required=True)
    location = db.StringField() # mongoengine does not support geolocation fields
    position_id = db.ObjectIdField(required=True)
    user_userAttended = db.BooleanField()
