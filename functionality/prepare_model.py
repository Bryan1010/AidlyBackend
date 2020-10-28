import pandas as pd
from pandas import DataFrame
from pycaret.nlp import *
from mainapp import db
from models.companies import Company, CompanyAddress
from models.topics import Topic, CompanyTopic, UserTopic
from models.interests import Interest, TopicInterest, CompanyInterest, UserInterest
from models.users import User
from models.matches import Matches
from datetime import datetime
from models import *

def importStartData():
    data = pd.read_csv("/home/aidly/aidlyapi/starting_data/start_data.csv")
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
            city=row['City'], state=row['State'], zip=row['Zip'], country='US', is_primary=True)

        
        db.session.add(rowCompany)
        db.session.add(address)
        db.session.commit()
        
    data = pd.read_csv("/home/aidly/aidlyapi/starting_data/ngo_berks.csv")
    for index, row in data.iterrows():
        rowCompany = Company(name=row['Name'], mission_statement=row['Mission_Statement'],
            main_email = row['Email'], primary_phone = row['Phone'], active = True)
            
        address = CompanyAddress(company=rowCompany, address1=row['address1'], address2=row['address2'], address3=row['address3'],
            city=row['city'], state=row['state'], zip=row['zip'], country=row['country'], is_primary=True)
 
        db.session.add(rowCompany)
        db.session.add(address)
        db.session.commit()
    
    
    data = pd.read_csv("/home/aidly/aidlyapi/starting_data/ngo_centre.csv")
    for index, row in data.iterrows():
        rowCompany = Company(name=row['Name'], mission_statement=row['Mission_Statement'],
            main_email = row['Email'], primary_phone = row['Phone'], active = True)
 
        address = CompanyAddress(company=rowCompany, address1=row['address1'], address2=row['address2'], address3=row['address3'],
            city=row['city'], state=row['state'], zip=row['zip'], country=row['country'], is_primary=True)
            
        db.session.add(rowCompany)
        db.session.add(address)
        db.session.commit()

def createModel():
    nlp = setup(data = pd.read_sql(sql = db.session.query(Company).with_entities(Company.mission_statement).statement, con = db.session.bind), target = 'mission_statement', session_id = 1, custom_stopwords = ['provide', 'promote'])
    lda = create_model('lda', num_topics = 30, multi_core = True)
    #lda = tune_model(model = 'lda', multi_core= True)
    save_model(lda, './lda_history/lda_'+datetime.now().strftime('%Y%m%d%H%M%S%f'))
    save_model(lda, 'lda')
    
    
def dictToInterest():
    lda = load_model('lda')
    for v in lda.id2word.id2token.values():
        exists = db.session.query(db.exists().where(Interest.name == v)).scalar()
        if not exists:
            i = Interest(name=v)
            db.session.add(i)
            db.session.commit()

def topicsToDB():
    lda = load_model('lda')
    for i in range(lda.num_topics):
        topic = Topic(name = 'Topic ' + str(i+1))
        db.session.add(topic)
        db.session.commit()
        
def topicInterests():
    lda = load_model('lda')
    for i in range(lda.num_topics):
        ti = lda.show_topic(i)
        for t in ti:
            interest = Interest.query.filter_by(name=t[0]).first()
            tim = TopicInterest(topic_id=(i+1), interest_id=interest.id)
            db.session.add(tim)
            db.session.commit()

def userInterests():
    user = User(first_name='Derek', last_name='DeTommaso', email='derek@derekstephen.dev', password='112', phone_number='9733625479', zip='19607', mission_statement='I want to work with children and animals.')
    db.session.add(user)
    db.session.commit()
    interests = ['wounded warriors','cyber security', 'information technology', 'football', 'cooking', 'baseball', 'education', 'patriotism']
    user = User.query.filter_by(email='derek@derekstephen.dev').first()
    for c, n in enumerate(interests):
        exists = db.session.query(db.exists().where(Interest.name == n)).scalar()
        if not exists:
            interest = Interest(name=n)
            db.session.add(interest)
            db.session.commit()
        interest = Interest.query.filter_by(name=n).first()
        db.session.add(UserInterest(user_id=user.id, interest_id=interest.id))
        db.session.commit()
    
def userTopics():
    user = User.query.filter_by(email='derek@derekstephen.dev').first()
    userinterests = UserInterest.query.filter_by(user_id=user.id).all()
    list_interests = []
    for ui in userinterests:
        i = Interest.query.filter_by(id=ui.interest_id).first()
        list_interests.append(i.name)
    
    list_interests.append(user.mission_statement)
    
    df_int = DataFrame(list_interests, columns = ['interests'])
    
    
    
    lda = load_model('lda')
    setup(data = df_int, target='interests')
    lda_df = assign_model(lda)
    
    topics_done = []
    for index, row in lda_df.iterrows():
        exists = db.session.query(db.exists().where(Topic.name == row['Dominant_Topic'])).scalar()
        if exists:
            t = Topic.query.filter_by(name = row['Dominant_Topic']).first()
            if t.id not in topics_done:
                db.session.add(UserTopic(user_id=user.id, topic_id=t.id, perc=row['Perc_Dominant_Topic']))
                db.session.commit()
                topics_done.append(t.id)

def userTopics(user):
    userinterests = UserInterest.query.filter_by(user_id=user.id).all()
    list_interests = []
    for ui in userinterests:
        i = Interest.query.filter_by(id=ui.interest_id).first()
        list_interests.append(i.name)
    
    list_interests.append(user.mission_statement)
    
    df_int = DataFrame(list_interests, columns = ['interests'])
    
    
    
    lda = load_model('lda')
    setup(data = df_int, target='interests')
    lda_df = assign_model(lda)
    
    topics_done = []
    for index, row in lda_df.iterrows():
        exists = db.session.query(db.exists().where(Topic.name == row['Dominant_Topic'])).scalar()
        if exists:
            t = Topic.query.filter_by(name = row['Dominant_Topic']).first()
            if t.id not in topics_done:
                db.session.add(UserTopic(user_id=user.id, topic_id=t.id, perc=row['Perc_Dominant_Topic']))
                db.session.commit()
                topics_done.append(t.id)

def companyInterests():
    pass

def companyTopics():
    lda = load_model('lda')
    setup(data = pd.read_sql(sql = db.session.query(Company).with_entities(Company.name, Company.mission_statement).statement, con = db.session.bind), target = 'mission_statement', session_id = 1, custom_stopwords = ['provide', 'promote'])
    lda_df = assign_model(lda)
    
    
    for index, row in lda_df.iterrows():
        exists = db.session.query(db.exists().where(Topic.name == row['Dominant_Topic'])).scalar()
        if exists:
            t = Topic.query.filter_by(name = row['Dominant_Topic']).first()
            c = Company.query.filter_by(name=row['name']).first()
            
            if db.session.query(db.exists().where(CompanyTopic.company_id==c.id)).scalar():
                current_t = CompanyTopic.query.filter_by(company_id=c.id).first()
                if current_t.perc < row['Perc_Dominant_Topic']:
                    db.session.delete(current_t)
                    db.session.add(CompanyTopic(company_id=c.id, topic_id=t.id, perc=row['Perc_Dominant_Topic']))
                    db.session.commit()
                    
            else:
                db.session.add(CompanyTopic(company_id=c.id, topic_id=t.id, perc=row['Perc_Dominant_Topic']))
                db.session.commit()
            
    
def userMatches():
    u = User.query.filter_by(email='derek@derekstephen.dev').first()
    ut = UserTopic.query.filter_by(user_id=u.id).all()
    ct = CompanyTopic.query.all()
    
    list_ut = []
    list_ut_p = []
    for t in ut:
        list_ut.append('Topic ' + str(t.topic_id))
        list_ut_p.append(t.perc)
    
    
    active_match = 0
    inactive_match = 0
    total = 0
    list_ct = []
    for c in ct:
        total = total + 1
        if(("Topic " + str(c.topic_id)) in list_ut):
            comp = Company.query.filter_by(id=c.company_id).first()
                     
            if comp.active:
                db.session.add(Matches(company_id=c.company_id, user_id=u.id, company_perc=c.perc, user_perc=list_ut_p[list_ut.index(("Topic " + str(c.topic_id)))]))
                db.session.commit()
                active_match = active_match + 1
            else:
                inactive_match = inactive_match + 1
            
def userMatches(u):
    ut = UserTopic.query.filter_by(user_id=u.id).all()
    ct = CompanyTopic.query.all()
    
    list_ut = []
    list_ut_p = []
    for t in ut:
        list_ut.append('Topic ' + str(t.topic_id))
        list_ut_p.append(t.perc)
    
    
    active_match = 0
    inactive_match = 0
    total = 0
    list_ct = []
    for c in ct:
        total = total + 1
        if(("Topic " + str(c.topic_id)) in list_ut):
            comp = Company.query.filter_by(id=c.company_id).first()
                     
            if comp.active:
                exists = db.session.query(db.exists().where(Matches.user_id == u.id).where(Matches.company_id==c.company_id)).scalar()
                if not exists:
                    db.session.add(Matches(company_id=c.company_id, user_id=u.id, company_perc=c.perc, user_perc=list_ut_p[list_ut.index(("Topic " + str(c.topic_id)))]))
                    db.session.commit()
                    active_match = active_match + 1
            else:
                inactive_match = inactive_match + 1
    print('Active: ', active_match)
    print('Inactive: ', inactive_match)
    print('Total: ', total)
    

def main():
    
    print('-- RESET DB --')
    db.drop_all()
    db.create_all()
    importStartData()
    print('-- DB RESET DONE --')
    
    print('-- START CREATE MODEL --')
    createModel()
    print('-- END CREATE MODEL --')
    
    print('-- START Dict TO Interest DB --')
    dictToInterest()
    print('-- END Dict TO Interest DB --')
    
    print('-- START TOPICS TO DB --')
    topicsToDB()
    print('-- END TOPICS TO DB --')
    
    print('-- START topicInterests TO DB --')
    topicInterests()
    print('-- END topicInterests TO DB --')
    
    print('-- START userInterests TO DB --')
    userInterests()
    print('-- END userInterests TO DB --')
    
    user = User.query.filter_by(email='derek@derekstephen.dev').first()
    
    print('-- START userTopics TO DB --')
    userTopics(user)
    print('-- END userTopics TO DB --')
    
    print('-- START companyInterests TO DB --')
    companyInterests()
    print('-- END companyInterests TO DB --')
    
    print('-- START companyTopics TO DB --')
    companyTopics()
    print('-- END companyTopics TO DB --')
    
    print('-- START userMatches TO DB --')
    userMatches(user)
    print('-- END userMatches TO DB --')
    
    
    
    