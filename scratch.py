from mainapp import MAIN_APP
from models import *
from models.users import User

# initialize connection to DB
from mainapp import db

# Create Tables on DB
db.create_all()

# try to create dummy user
user = User(email='yo@lo.co', first_name='bryan', last_name='cruz', password='password')
user.hash_password()
user2 = User(email='second@email.com', first_name='Joe', last_name='Chill', password='password')
user2.hash_password()

db.session.add(user)
db.session.add(user2)
db.session.commit()

# try to create an interest
from models.users import Interest

interest = Interest(interest_name='Photography')
db.session.add(interest)
db.session.commit()

interest2 = Interest(interest_name='Technology')
db.session.add(interest2)
db.session.commit()

# create UserInterest
from models.users import UserInterest

userInterest = UserInterest(user=user, interest=interest)
db.session.add(userInterest)
db.session.commit()

userInterest2 = UserInterest(user=user2, interest=interest2)
db.session.add(userInterest2)
db.session.commit()

userInterest3 = UserInterest(user=user, interest=interest2)
db.session.add(userInterest3)
db.session.commit()

# Retrieve Data
# 1. get a user
retrieved_user1 = User.query.filter_by(id=1).first()
retrieved_user2 = User.query.filter_by(id=2).first()

# get interests for user
print('get interests for user id 1')
# Get list of interests
user1_interests = retrieved_user1.interests
print(user1_interests)
# get interest name
user1_interest1_name = user1_interests[0].interest.interest_name
user1_interest2_name = user1_interests[1].interest.interest_name
print(f'Interest 1 = {user1_interest1_name}')
print(f'Interest 2 = {user1_interest2_name}')

from models.companies import *

# Create a company
company = Company(name='Big Brothers')
db.session.add(company)
db.session.commit()

# add user as a company admin
companyUser = CompanyUsers(company=company, user=user, is_admin=True)
db.session.add(companyUser)
db.session.commit()
