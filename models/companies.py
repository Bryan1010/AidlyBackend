from models import db

COMPANY_TYPES = ('NGO', 'Company')

class Company(db.Document):
    CompanyName = db.StringField(required=True)
    Type = db.StringField(choices=COMPANY_TYPES)
    LogoUrl = db.StringField
    PrimaryColor = db.StringField
    SecondaryColor = db.StringField

    meta ={
        'collection': 'companies'
    }