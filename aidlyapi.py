from mainapp import MAIN_APP
# from models.company import Company
from flask import request, Response
from models import db

@MAIN_APP.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    MAIN_APP.run(host='0.0.0.0')
