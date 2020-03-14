from models import db

from models.positions import Position

COMPANY_TYPES = ('NGO', 'Company')

class Company(db.Document):
    CompanyName = db.StringField(required=True)
    Type = db.StringField(choices=COMPANY_TYPES)
    LogoUrl = db.StringField
    PrimaryColor = db.StringField
    SecondaryColor = db.StringField

    positions = db.EmbeddedDocumentListField(Position)


    meta ={
        'collection': 'companies'
    }