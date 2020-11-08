from flask import Blueprint, Response, request, json, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy.sql import label
from models import  db
from models.companies import Company, CompanyAddress
from models.users import User
from models.matches import Matches

company_blueprint = Blueprint('company', __name__)

@company_blueprint.route('/')
def hello_world():
    return 'Hello, Aidly User !'

@company_blueprint.route('/all', methods=['GET'] )
def get_all_companies():
    allCompanies = Company.query.all()
    orgList = [ngo.to_dict() for ngo in allCompanies]
    return jsonify(organizations = orgList)

@company_blueprint.route('/countCompanyMatches', methods=['GET'])
def get_all_companies_matches():
    return jsonify(matches = 100)

@company_blueprint.route('/companyusersmatches', methods=['GET'])
def get_all_companies_user_matches():
    allUsers = User.query.all()
    userList = [us.to_dict() for us in allUsers]
    return jsonify(users = userList)

@company_blueprint.route('/add', methods=['POST'])
def add_company():
    return 'need to implement'

@company_blueprint.route('/update', methods=['GET'])
def get_company():
    allCompanies = Company.query.filter_by(active=True).first()
    return jsonify(companies = allCompanies.to_dict())

@company_blueprint.route('/update', methods=['POST'])
def udpate_company():
    post_data = request.get_json()
    comp = Company.query.filter_by(id = post_data.get('id'))
    comp.name = post_data.get('name')
    comp.primary_phone = post_data.get('primary_phone')
    comp.main_email = post_data.get('main_email')
    comp.ein = post_data.get('ein')
    comp.mission_statement = post_data.get('mission_statement')
    # db.session.add(comp)
    db.session.commit()
    return ''

@company_blueprint.route('/matches', methods=['GET'])
def get_company_mathces_for_user():
    print(request.headers)
    # Needs Auth Header
    # Authorization: Bearer TOKENHERE
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''
        responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
        return make_response(jsonify(responseObject)), 401

    # Get current user that made the request
    try:
        user = User.query.filter_by(id= User.decode_auth_token(auth_token)).first()
        if user is None:
            raise NoResultFound('no results found')
    except NoResultFound:
        return jsonify({'organizations': []}), 401
    user = User.query.filter_by(id= User.decode_auth_token(auth_token)).first()
    zipcode = int(user.zip)
    accepted_zips = []
    for i in range(zipcode, zipcode + 10):
        accepted_zips.append(i)
        
    for i in range(zipcode, zipcode - 10, -1):
        accepted_zips.append(i)
    
    usermatches = Matches.query.filter_by(user_id=user.id).order_by(Matches.user_perc.desc(),Matches.company_perc.desc()).all()
    matches = [m.to_dict() for m in usermatches]
    companies = []
    counter = 0
    for match in usermatches:
        
        if(counter > 3):
            break
        c = Company.query.filter_by(id=match.company_id).first()
        ca = CompanyAddress.query.filter_by(id=match.company_id).first()
        
        zipc = 0
        
        try:
            zipc = int(ca.zip)
        except ValueError:
            zipc = -9999
        
        if zipc in accepted_zips:
            counter = counter+1
            info = {}
            info['id'] = c.id
            info['name'] = c.name
            if c.main_email:
                info['main_email'] = c.main_email.strip()
            else:
                info['main_email'] = ""
            if c.ein:
                info['ein'] = c.ein
            else:
                info['ein'] = ""
            if c.primary_phone:
                info['phone'] = c.primary_phone
            else:
                info['phone'] = ""
            
            ump = match.user_perc * 100
            cmp = match.company_perc * 100
            
            if ump > 70:
                info['percentage_match'] = "Strong"
            elif ump > 50:
                info['percentage_match'] = "Average"
            else:
                info['percentage_match'] = "Weak"
            
            
            
            c_a = CompanyAddress.query.filter_by(company_id=c.id).first()
            
            
            if c_a:
                if c_a.address1:
                    info['street'] = c_a.address1
                else:
                    info['street'] = ""
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
        
    if counter == 0:
        info = {}
        
        info['name'] = "Oh no... we couldn't find any matches for you, but we will keep looking!"
        
        companies.append(info)
    
    return make_response(jsonify(organizations=companies)), 200

    
@company_blueprint.route('/userMatches', methods=['GET'])
def get_user_matches():
    orgList = [
        {'name': 'Big brothers', 'main_email': 'email@bbss.org', 'ein': '3982147985867', 'percentage_match': 75.5,
            'address1': '2nd street',
            'address2': '',
            'address3':'',
            'city': 'Reading',
            'state': 'PA',
            'country': 'US',
            'zip': '19608',
            'primary_phone': '787-568-6062'
        },
        {'name': 'Non profit 2', 'main_email': 'email@free.org', 'ein': '123456789', 'percentage_match': 90,
            
            'address1': '1st street',
            'address2': '',
            'address3':'',
            'city': 'Reading',
            'state': 'PA',
            'country': 'US',
            'zip': '19608',
            'primary_phone': '484-888-6655'
        },
        {'name': 'Non profit 3', 'main_email': 'email@free3.org', 'ein': '5432453', 'percentage_match': 98,
            
            'address1': '3rd street',
            'address2': '',
            'address3':'',
            'city': 'Reading',
            'state': 'PA',
            'country': 'US',
            'zip': '19608',
            'primary_phone': '484-888-6655'
        }
    ]
    return jsonify(organizations = orgList), 200
