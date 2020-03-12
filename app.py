import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Resource, Api


load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('DB')
api = Api(app)

@app.route('/')
def hello_world():
    return 'Hello, Aidly !'


class Opportunity(Resource):
    def get(self,num):
        return {
            'result': num*2
            }

api.add_resource(Opportunity, '/opportunity/<int:num>')


if(__name__ == "__main__"):
    app.run(debug=True, port=1234)