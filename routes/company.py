from flask import Blueprint, Response, request, json, jsonify, make_response
from models.companies import Company

company_blueprint = Blueprint('company', __name__)

@company_blueprint.route('/')
def hello_world():
    return 'Hello, Aidly User !'

@company_blueprint.route('/all', methods=['GET'] )
def get_company():
    return 'neet to implement'


@company_blueprint.route('/add', methods=['post'])
def add_company():
    return 'need to implement'