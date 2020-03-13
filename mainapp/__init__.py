'''
Main App Initialization
'''
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

MAIN_APP = Flask(__name__)

from models import initialize_db

MAIN_APP.config['MONGODB_SETTINGS'] = {
    'host': os.environ.get('DB')
}
initialize_db(MAIN_APP)

from routes.company import company_blueprint

MAIN_APP.register_blueprint(company_blueprint, url_prefix='/company')