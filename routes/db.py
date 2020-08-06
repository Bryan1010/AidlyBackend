from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User
from models.interests import Interest, UserInterest
from sqlalchemy.orm.exc import NoResultFound
from models import db
from models.blacklistTokens import BlacklistToken
import base64
from models.companies import *
from models.topics import *
from models import *

db_blueprint = Blueprint('db', __name__)

@db_blueprint.route('/createDB', methods=['GET'])
def create_database():
    db.create_all()
    return 'Database Tables Created'
    
@db_blueprint.route('/deleteDB', methods=['GET'])
def delete_database():
    db.drop_all()
    return 'Database Tables Dropped'