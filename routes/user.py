from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User, UserInterest
# from models.Interests import Interest, UserInterest
from models import  db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/yolozurc', methods=['GET'] )
def get_company():
    user = User(first_name='bryan', last_name='cruz', email='b@ca.com')
    db.session.add(user)
    db.session.commit()
    return 'added new user!'

@user_blueprint.route('/getyolo/<email>', methods=['GET'] )
def get_user(email):
    user = User.query.filter_by(email=email).first()
    # interest = UserInterest.query.filter_by(user=user)


    return f'The User\'s name is: { user.get_full_name() } '