import pandas as pd
from mainapp import db
from models.companies import *
from models.topics import *
from models import *


def importStartData():
    data = pd.read_csv("/var/www/apache_html/apache_html/starting_data/start_data.csv")
    data = data[['NAME', 'F9_03_PZ_MISSION', 'Orgemail','Address','City','State','Zip','Primarycontactphone']]
    data = data.dropna()
    data['F9_03_PZ_MISSION'] = data['F9_03_PZ_MISSION'].apply(lambda x: x.replace('NBSP;', ''))
    data = data[data.F9_03_PZ_MISSION != 'NONE']
    data = data[data.NAME != "Serenity Sista's Inc"]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("SCHEDULE O")]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("Schedule O")]
    data = data[~data["F9_03_PZ_MISSION"].str.contains("SEE ATTACHED COPY OF MISSION STATEMENT")]

    for index, row in data.iterrows():
        rowCompany = Company(name=row['NAME'], mission_statement=row['F9_03_PZ_MISSION'],
            main_email = row['Orgemail'], primary_phone = row['Primarycontactphone'])
        
        address = CompanyAddress(company=rowCompany, address1=row['Address'],
            city=row['City'], state=row['State'], zip=row['Zip'], is_primary=True)

        
        db.session.add(rowCompany)
        db.session.add(address)
        db.session.commit()
        
    data = pd.read_csv("/var/www/apache_html/apache_html/starting_data/ngo_berks.csv")
    for index, row in data.iterrows():
        rowCompany = Company(name=row['Name'], mission_statement=row['Mission_Statement'],
            main_email = row['Email'], primary_phone = row['Phone'])
 
        db.session.add(rowCompany)
        db.session.commit()
    
    
    data = pd.read_csv("/var/www/apache_html/apache_html/starting_data/ngo_centre.csv")
    for index, row in data.iterrows():
        rowCompany = Company(name=row['Name'], mission_statement=row['Mission_Statement'],
            main_email = row['Email'], primary_phone = row['Phone'])
 
        db.session.add(rowCompany)
        db.session.commit()

# Create Tables on DB
db.create_all()

importStartData()

print()
