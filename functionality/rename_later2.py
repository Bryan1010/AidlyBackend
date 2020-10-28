import pandas as pd
from pycaret.nlp import *
from mainapp import db
from models.companies import Company
from datetime import datetime

df_berks = pd.read_csv('ngo_berks.csv')
df_centre = pd.read_csv('ngo_centre_county.csv')

#ngo = pd.concat([df_berks, df_centre])

lda = load_model('lda')
nlp = setup(data = pd.read_sql(sql = db.session.query(Company).with_entities(Company.name, Company.mission_statement).statement, con = db.session.bind), target = 'mission_statement', session_id = 1, custom_stopwords = ['provide', 'promote'])
lda_df = assign_model(lda)

print(lda_df)
lda_df.to_csv(r'/var/www/apache_html/apache_html/topics_ngo.csv')

nlp = setup(data = df_centre, target = 'Mission_Statement', session_id = 1, custom_stopwords = ['provide', 'promote'])
lda_df = assign_model(lda)
lda_df.to_csv(r'/var/www/apache_html/apache_html/topics_centre.csv')

nlp = setup(data = df_berks, target = 'Mission_Statement', session_id = 1, custom_stopwords = ['provide', 'promote'])
lda_df = assign_model(lda)
lda_df.to_csv(r'/var/www/apache_html/apache_html/topics_berks.csv')
