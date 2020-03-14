from models import db

class Position(db.EmbeddedDocument):
    company_id = db.ObjectIdField(required=True)
    description = db.StringField()
    interests = db.ListField(db.StringField())
    requirements = db.ListField(db.StringField())
    