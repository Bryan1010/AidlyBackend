from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User
from sqlalchemy.orm.exc import NoResultFound
from models import db
from models.blacklistTokens import BlacklistToken
import base64
from models.companies import *
from models.topics import *
from models import *
import pandas as pd
from pycaret.nlp import *
from pycaret import *
from models.users import User
from models.matches import *
from models.interests import *
from pandas import DataFrame

dev_blueprint = Blueprint('dev', __name__)

@dev_blueprint.route('/createDB', methods=['GET'])
def create_database():
    db.create_all()
    return 'Database Tables Created'

@dev_blueprint.route('/deleteDB', methods=['GET'])
def delete_database():
    db.drop_all()
    return 'Database Tables Dropped'

@dev_blueprint.route('/fakeUser', methods=['GET'])
def fake_user():
    user = User(first_name='Derek', last_name='DeTommaso', email='derek@derekstephen.dev', password='112')
    db.session.add(user)
    db.session.commit()
    interests = ['wounded warriors','cyber security', 'information technology', 'football', 'cooking', 'baseball', 'education', 'patriotism']
    user = User.query.filter_by(email='derek@derekstephen.dev').first()
    for c, n in enumerate(topics):
        topic = Topic(name=n)
        db.session.add(topic)
        db.session.commit()
        db.session.add(UserTopic(user_id=user.id, topic_id=c+1))
        db.session.commit()
    return 'added new user and topics!'

@dev_blueprint.route('/byederek', methods=['GET'])
def remove_company():
    user = User.query.filter_by(email='derek@derekstephen.dev').first()
    db.session.delete(user)
    db.session.commit()
    return 'deleted new user!'

@dev_blueprint.route('/defaultData', methods=['GET'])
def fill_companies():
    def importStartData():
        data = pd.read_csv("start_data.csv")
        data = data[['NAME', 'F9_03_PZ_MISSION', 'Orgemail','Address','City','State','Zip','Primarycontactphone']]
        data = data.dropna()
        data['F9_03_PZ_MISSION'] = data['F9_03_PZ_MISSION'].apply(lambda x: x.replace('NBSP;', ''))
        data = data[data.F9_03_PZ_MISSION != 'NONE']
        data = data[data.NAME != "Serenity Sista's Inc"]
        data = data[~data["F9_03_PZ_MISSION"].str.contains("SCHEDULE O")]
        data = data[~data["F9_03_PZ_MISSION"].str.contains("Schedule O")]
        data = data[~data["F9_03_PZ_MISSION"].str.contains("SEE ATTACHED COPY OF MISSION STATEMENT")]

        for index, row in data.iterrows():
            rowCompany = Company(name=row['NAME'], mission_statement=row['F9_03_PZ_MISSION'],
                main_email = row['Orgemail'], primary_phone = row['Primarycontactphone'])
            
            address = CompanyAddress(company=rowCompany, address1=row['Address'],
                city=row['City'], state=row['State'], zip=row['Zip'], is_primary=True)


            db.session.add(rowCompany)
            db.session.add(address)
            db.session.commit()

    importStartData()
    return 'Companies Table Filled'
    
# TODO: CLEAN CODE UP LATER 
@dev_blueprint.route('/matchesAll', methods=['GET'])
def matchesAll():
    user = User.query.filter_by(email=request.args['email']).first()
    usermatches = Matches.query.filter_by(user_id=user.id).order_by(Matches.user_perc.desc(),Matches.company_perc.desc()).all()
    matches = [m.to_dict() for m in usermatches]
    companies = []
    for match in usermatches:
        c = Company.query.filter_by(id=match.company_id).first()
        info = {}
        info['id'] = c.id
        info['name'] = c.name
        info['active'] = c.active
        if c.main_email:
            info['main_email'] = c.main_email
        else:
            info['main_email'] = ""
        if c.main_email:
            info['ein'] = c.ein
        else:
            info['ein'] = ""
        if c.main_email:
            info['primary_phone'] = c.primary_phone
        else:
            info['primary_phone'] = ""
        
        info['percentage_match'] = 0
        c_a = CompanyAddress.query.filter_by(company_id=c.id).first()
        if c_a:
            if c_a.address1:
                info['address1'] = c_a.address1
            else:
                info['address1'] = ""
            if c_a.address2:
                info['address2'] = c_a.address2
            else:
                info['address2'] = ""
            if c_a.address3:
                info['address3'] = c_a.address3
            else:
                info['address3'] = ""
            if c_a.city:
                info['city'] = c_a.city
            else:
                info['city'] = ""
            if c_a.state:
                info['state'] = c_a.state
            else:
                info['state'] = ""
            if c_a.zip:
                info['zip'] = c_a.zip
            else:
                info['zip'] = ""
            if c_a.country:
                info['country'] = c_a.country
            else:
                info['country'] = ""
        else:
            info['address1'] = ""
            info['address2'] = ""
            info['address3'] = ""
            info['city'] = ""
            info['state'] = ""
            info['zip'] = ""
            info['country'] = ""
        
        
        companies.append(info)
    
    
    return make_response(jsonify(organizations=companies)), 200

@dev_blueprint.route('/matchesTwo', methods=['POST'])
def matchesTwo():
    user = User.query.filter_by(email=request.args['email']).first()
    usertopics = UserTopic.query.filter_by(user_id=user.id).order_by(UserTopic.perc).all()
    usermatches = Matches.query.filter_by(user_id=user.id).all()
    matches = [m.to_dict() for m in usermatches]
    companies = []
    
    
    
    
    
    return make_response(jsonify(matches)), 200


@dev_blueprint.route('/runModelCompanies', methods=['GET'])
def load_model():
    lda = nlp.load_model('lda')
    
    return 'model loaded'

@dev_blueprint.route('/runModel', methods=['GET'])
def use_model():
    interests = ['wounded warriors','cyber security', 'information technology', 'football', 'cooking', 'baseball', 'education', 'patriotism']
    df_int = DataFrame(interests, columns=['interests'])
    lda = nlp.load_model('lda')
    
    
    setup(data = df_int)
    lda_df = assign_model(lda)
    return lda_df
    
    
@dev_blueprint.route('/percentages', methods=['GET'])
def percentages():
    allCompaniesTopics = CompanyTopic.query.all()
    allUsersTopics = UserTopic.query.all()
    act = [ct.to_dict() for ct in allCompaniesTopics]
    aut = [ut.to_dict() for ut in allUsersTopics]
    
    
    
    return make_response(jsonify(CompanyTopics = act, UserTopics = aut))
    
