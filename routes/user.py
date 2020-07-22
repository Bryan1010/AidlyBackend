from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User
from models.interests import Interest, UserInterest
from sqlalchemy.orm.exc import NoResultFound
from models import  db
from models.blacklistTokens import BlacklistToken
import base64

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/yolozurc', methods=['GET'] )
def get_company():
    user = User(first_name='bryan', last_name='cruz', email='b@ca.com', password='password')
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
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            user = User(
                email=post_data.get('email'),
                password=post_data.get('password')
            )

            # insert the user
            db.session.add(user)
            db.session.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

@user_blueprint.route('/tokenStatus', methods=['POST'])
def check_token():
    # get the auth token
    # Header needs to have a Authorization: Bearer TOKEN_HERE
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
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'registered_on': user.date_created
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401

@user_blueprint.route('/token', methods=['POST'])
def get_token():
    user_email = request.json.get('email')
    user_pass = request.json.get('password')
    try:
        user = User.query.filter_by(email=user_email).first()
    except NoResultFound:
        return jsonify({'token': ''}), 401

    # need to decode to ascii to get non-byte token
    token = base64.b64encode(user.generate_auth_token()).decode('ascii')
    
    # If password is correct, return auth token
    if User.check_password(self=user, password=user_pass):
        return jsonify(token= token), 200
    else:
        return jsonify({'token': ''}), 401

@user_blueprint.route('/login', methods=['POST'])
def Login():
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and user.check_password(post_data.get('password')):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500

@user_blueprint.route('/logout', methods=['POST'])
def Logout():
    # get auth token
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
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403