from models import db

from models.appointments import Appointment


class User(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.StringField(required=True)
    mission_statement = db.StringField()
    interests = db.ListField(db.StringField())
    time_availability = db.ListField(db.DateTimeField())

    appointments = db.EmbeddedDocumentListField(Appointment)

    meta ={
        'collection': 'users'
    }