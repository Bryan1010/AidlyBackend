from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User, UserInterest
# from models.Interests import Interest, UserInterest
from sqlalchemy.orm.exc import NoResultFound
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


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    return ''


@user_blueprint.route('/token', methods=['POST'])
def get_token():
    user_email = request.json.get('email')
    user_pass = request.json.get('password')
    try:
        user = User.query.filter_by(email=user_email).first()
    except NoResultFound:
        return jsonify({'token': ''}), 401

    # If password is correct, return auth token
    if User.check_password(self=user, password=user_pass):
        return jsonify({'token': user.generate_auth_token()}), 200
    else:
        return jsonify({'token': ''}), 401

