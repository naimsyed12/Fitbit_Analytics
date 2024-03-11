import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import os
import psycopg2

postgre_password = os.getenv('Postgre')
fitbit = pd.read_csv('steps_df.csv')
apple = pd.read_csv('total_steps.csv')

fitbit.rename({'value':'Fitbit_Steps'},axis=1, inplace=True)
apple.rename({'value':'Apple_Steps'},axis=1, inplace=True)

combined = fitbit.merge(apple,how='left',on='dateTime')
combined['steps']=np.where(combined['Fitbit_Steps'] == 0, combined['Apple_Steps'], combined['Fitbit_Steps'])

connection_string = 'postgresql+psycopg2://postgres:'+postgre_password+'@localhost:5432/Health_Analytics'
db = create_engine(connection_string)
connection = db.connect()
combined.to_sql('steps', con=connection,if_exists='replace',index = False)



