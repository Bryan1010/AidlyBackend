from flask import Blueprint, Response, request, json, jsonify, make_response
from models.users import User
from models.interests import Interest, UserInterest
from sqlalchemy.orm.exc import NoResultFound
from models import db
from models.blacklistTokens import BlacklistToken
from datetime import datetime, timedelta
from functionality import prepare_model
import base64

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def hello_world():
    return 'Hello, Aidly User !'

@user_blueprint.route('/yolozurc', methods=['GET'] )
def get_company():
    user = User(first_name='bryan', last_name='cruz', email='b@ca.com', password='password',phone_number='123-123-123',zip='00959')
    db.session.add(user)
    db.session.commit()
    return 'added new user!'

@user_blueprint.route('/byezurc', methods=['GET'] )
def remove_company():
    user = User(first_name='bryan', last_name='cruz', email='b@ca.com', password='password')
    db.session.delete(user)
    db.session.commit()
    return 'deleted new user!'

@user_blueprint.route('/get', methods=['POST'] )
def get_user():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data.get('email')).first()
    # interest = UserInterest.query.filter_by(user=user)

    return f'The User\'s name is: { user.get_full_name() } '

@user_blueprint.route('/interest', methods=['POST'] )
def add_interest():

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
        return jsonify({'interests': []}), 401
    user = User.query.filter_by(id= User.decode_auth_token(auth_token)).first()

    post_data = request.get_json()
    interests = post_data["interests"]

    interestAdded = False

    for n in interests:
        exists = db.session.query(db.exists().where(Interest.name == n)).scalar()
        if not exists:
            interest = Interest(name=n)
            db.session.add(interest)
            db.session.commit()
            interestAdded=True
        interest = Interest.query.filter_by(name=n).first()
        exists = db.session.query(db.exists().where(UserInterest.user_id == user.id).where(UserInterest.interest_id == interest.id)).scalar()
        if not exists:
            db.session.add(UserInterest(user_id=user.id, interest_id=interest.id))
            interestAdded=True

    db.session.commit()
    
    if interestAdded:
        prepare_model.userTopics(user)
        prepare_model.userMatches(user)

    return jsonify(message='Added Interests'), 200

@user_blueprint.route('/interest', methods=['GET'] )
def get_interest():

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
        userinterests = UserInterest.query.filter_by(user_id=user.id).all()
        if userinterests is None:
            raise NoResultFound('no results found')
    except NoResultFound:
        return jsonify({'interests': []}), 401


    list_interests = []
    for ui in userinterests:
        i = Interest.query.filter_by(id=ui.interest_id).first()
        list_interests.append(i.name)
    
    return jsonify(interests=list_interests), 200

@user_blueprint.route('/events', methods=['GET'] )
def get_user_events():
    events = [
        {
            'title': 'YMCA of Centre County Lunch',
            'date': datetime(2020,9, 14, 12,30).strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'YMCA of Centre County Lunch',
            'date': datetime(2020,9, 21, 12,30).strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'State College Food Bank Evening Volunteer',
            'date': datetime(2020,9, 24, 15,30).strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    return jsonify(events = events), 200

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
                password=post_data.get('password'),
                first_name=post_data.get('first_name'),
                last_name=post_data.get('last_name'),
                phone_number=post_data.get('phone_number'),
                mission_statement=post_data.get('mission_statement'),
                zip=post_data.get('zipcode')
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
        if user is None:
            raise NoResultFound('no results found')
    except NoResultFound:
        return jsonify({'token': ''}), 401

    # need to decode to ascii to get non-byte token
    token = base64.b64encode(user.generate_auth_token()).decode('ascii')
    
    # If password is correct, return auth token
    if User.check_password(self=user, password=user_pass):
        return jsonify(token=token, firstName=user.first_name, lastName=user.last_name), 200
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
                    'firstName': user.first_name,
                    'lastName': user.last_name,
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
            'message': 'Try again later'
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