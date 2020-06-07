from mainapp import MAIN_APP
# from models.company import Company
from flask import request, Response

@MAIN_APP.route('/')
def hello_world():
    return 'Hello, Aidly !'



if(__name__ == "__main__"):
    MAIN_APP.run(debug=True, port=1234)