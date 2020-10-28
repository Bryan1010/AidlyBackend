import pandas as pd
from pandas import DataFrame
from pycaret.nlp import *
#from models.users import User

interests = ['wounded warriors','cyber security', 'information technology', 'football', 'cooking', 'baseball', 'education', 'patriotism']
df_int = DataFrame(interests, columns=['interests'])
lda = load_model('lda')
#user = User.query.filter_by(email='derek@derekstephen.dev').first()


setup(data = df_int, target='interests')
lda_df = assign_model(lda)

print(lda_df)

