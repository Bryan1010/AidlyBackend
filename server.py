from mainapp import MAIN_APP
# from models.company import Company
from flask import request, Response
from models import db

@MAIN_APP.route('/')
def hello_world():
    return 'Hello, Aidly!<br>Go to db/createDB to create all tables<br>Go to db/deleteDB to drop all tables'


if(__name__ == "__main__"):
    MAIN_APP.run(host='0.0.0.0', debug=True, port=1234)
