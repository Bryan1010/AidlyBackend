from mainapp import MAIN_APP
from flask import request, Response

@MAIN_APP.route('/')
def hello_world():
    return 'Hello, Aidly!', 200

if __name__ == "__main__":
    MAIN_APP.run()
