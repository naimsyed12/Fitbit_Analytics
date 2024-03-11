import pandas as pd
import datetime as dt


def daily_steps(file):
    df = pd.read_csv(file,header=1,sep=';')
    df.drop(columns=['HKMetadataKeySyncVersion','HKMetadataKeySyncIdentifier'], inplace=True)
    #Reformat Start Date to YYYY-MM-DD
    df['dateTime']= pd.to_datetime(df['startdate']).dt.strftime('%Y-%m-%d')
    #Total Steps by Date
    total_steps = df[['value','dateTime']].groupby('dateTime').sum().reset_index()
    return total_steps.to_csv('total_steps.csv',index=False) 

file_path = 'apple_steps.csv'
daily_steps(file_path)
