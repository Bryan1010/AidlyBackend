from flask_sqlalchemy import SQLAlchemy
from mainapp import db as main_db

db = main_db


# def initialize_db(app):
#     db.init_app(app)
#     return app
#
#
# def create_db():
#     db.create_all()
