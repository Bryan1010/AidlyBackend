import mongoengine

COMPANY_TYPES = ('NGO', 'Company')

class Company(mongoengine.document):
    CompanyName = mongoengine.StringField(required=True)
    Type = mongoengine.StringField(choices=COMPANY_TYPES)
    LogoUrl = mongoengine.StringField
    PrimaryColor = mongoengine.StringField
    SecondaryColor = mongoengine.StringField

    meta ={
        'db_alias': 'db_conn',
        'collection': 'companies'
    }