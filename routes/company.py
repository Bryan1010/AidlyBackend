from flask import Blueprint, Response, request, json, jsonify, make_response
from models.company import Company

company_blueprint = Blueprint('company', __name__)

@company_blueprint.route('/all', methods=['GET'] )
def get_company():
    tmp = Company.objects().to_json()
    return  Response(tmp, mimetype="application/json", status=200)

@company_blueprint.route('', methods=['post'])
def add_company():
    body = request.get_json()
    
    comp = Company(**body).save()
    id = comp.id
    return {'id': str(id)}, 200