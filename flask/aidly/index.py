from flask import Flask, jsonify
from flask_pymongo import PyMongo
import os


 
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_CONN_STRING")
mongo = PyMongo(app)



@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route('/aidly/', methods=['GET'])
def get_tasks():
    return jsonify({'orgs': 'Boom'})