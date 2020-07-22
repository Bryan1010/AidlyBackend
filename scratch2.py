import pandas as pd
import texthero as hero
from mainapp import db
from models.companies import *

def uploadCompany(name="", logo_url="", primary_color="", secondary_color="", ein="", misson_statment=""):
    db.session.add(Company(name=name, mission_statement=misson_statment))
    db.session.commit()


def tokenizeCompanies():
    df = pd.read_sql(sql=db.session.query(Company).with_entities(Company.id, Company.name, Company.mission_statement).statement, con=db.session.bind)
    df['clean_mission'] = df['mission_statement'].pipe(hero.clean)
    df['tokenize'] = df['clean_mission'].pipe(hero.tokenize)
    return df




df = pd.read_csv("C:\\Users\\ddeto\\PycharmProjects\\AidlyAI\\Data\\berks_NGOs.csv")

df['clean_mission'] = df['Mission_Statement'].pipe(hero.clean)

df['tokenize'] = df['clean_mission'].pipe(hero.tokenize)



# initialize connection to DB


# Create Tables on DB
db.create_all()

for index, company in df.iterrows():
    uploadCompany(company['Name'], company['Mission_Statement'])





