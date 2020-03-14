from models import db

class Appointment(db.EmbeddedDocument):
    user_id = db.ObjectIdField(required=True)
    company_id = db.ObjectIdField(required=True)
    start_date = db.DateTimeField(required=True)
    location = db.StringField() # mongoengine does not support geolocation fields
    position_id = db.ObjectIdField(required=True)
    user_userAttended = db.BooleanField()
