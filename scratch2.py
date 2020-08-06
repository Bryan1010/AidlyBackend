import pandas as pd
from mainapp import db
from models.companies import *
from models.topics import *
from models import *


def importStartData():
    data = pd.read_csv("start_data.csv")
    data = data[['NAME', 'F9_03_PZ_MISSION']]
    data = data.dropna()
    data['F9_03_PZ_MISSION'] = data['F9_03_PZ_MISSION'].apply(lambda x: x.replace('NBSP;', ''))
    data = data[data.F9_03_PZ_MISSION != 'NONE']
    data = data[data.NAME != "Serenity Sista's Inc"]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("SCHEDULE O")]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("Schedule O")]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("SEE ATTACHED COPY OF MISSION STATEMENT")]
    for index, row in data.iterrows():
        db.session.add(Company(name=row['NAME'], mission_statement=row['F9_03_PZ_MISSION']))
        db.session.commit()


# Create Tables on DB
db.create_all()

importStartData()
