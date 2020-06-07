'''
Main App Initialization
'''
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

MAIN_APP = Flask(__name__)

MAIN_APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DBCONN')
MAIN_APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from models import initialize_db
#
# db = initialize_db(MAIN_APP)

db = SQLAlchemy(MAIN_APP)

from routes.user import user_blueprint
from routes.company import company_blueprint

MAIN_APP.register_blueprint(company_blueprint, url_prefix='/company')
MAIN_APP.register_blueprint(user_blueprint, url_prefix='/user')
