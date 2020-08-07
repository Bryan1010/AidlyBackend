from flask import Blueprint, Response, request, json, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
from models import  db
from models.companies import Company

company_blueprint = Blueprint('company', __name__)

@company_blueprint.route('/')
def hello_world():
    return 'Hello, Aidly User !'

@company_blueprint.route('/all', methods=['GET'] )
def get_company():
    allCompanies = Company.query.all()
    
    return allCompanies.__dict__


@company_blueprint.route('/add', methods=['post'])
def add_company():
    return 'need to implement'

    
@company_blueprint.route('/userMatches', methods=['GET'])
def get_user_matches():
    orgList = [
        {'name': 'Big brothers', 'main_email': 'email@bbss.org', 'ein': '3982147985867', 'percentage_match': 75.5,
            'address': {
                'street': '2nd street',
                'city': 'Reading',
                'state': 'PA',
                'zip': '19608'
            },
            'primary_phone': '787-568-6062'
        },
        {'name': 'Non profit 2', 'main_email': 'email@free.org', 'ein': '123456789', 'percentage_match': 90,
            'address': {
                'street': '1st street',
                'city': 'Reading',
                'state': 'PA',
                'zip': '19608'
            },
            'primary_phone': '484-888-6655'
        }        
    ]
    return jsonify(organizations = orgList), 200