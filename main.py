import json
import requests
import os                                                                                           
import Refresh
from datetime import date, timedelta, datetime
import pandas as pd
from API_Functions import loadtokens, Step_API, refresh_request, Weight_API


file_name = '../Credentials/accesstoken.json'                                                                                         

access_token, refresh_token, userid = loadtokens(file_name)
                               

#Create Date Range DataFrame for iteration
start_dates = list(pd.date_range(start=date(2019,6,1),end=pd.Timestamp.today().date(),freq='MS'))
end_dates = list(pd.date_range(start=date(2019,6,1),end=pd.Timestamp.today().date(),freq='M'))
yesterday = pd.Timestamp(datetime.today().date()-timedelta(days=1))
end_dates.append(yesterday)

datatypes = {"Start":"datetime64[ns]","End":"datetime64[ns]"}
dates = pd.DataFrame({'Start':start_dates,'End':end_dates}).astype(datatypes)
dates.to_csv('daterange.csv',index=False)

#Empty DataFrame to append with steps data throughout loop
steps_df = pd.DataFrame()

#Iterate through date range to retrieve, parse, and store Weight data
weight_values = []
weight_dates = []

for index,row in dates.iterrows():
    start_date=str(row['Start'].date())
    end_date=str(row['End'].date())
    #Run API
    api_status_code, weight_json = Weight_API(start_date,end_date, userid, access_token)
    print(f'API Date Parameters: Start = {start_date}, End = {end_date}') 
    if api_status_code==200:
        for key in range(0,len(weight_json['weight'])):
            weight_values.append(weight_json['weight'][key]['weight']) 
            weight_dates.append(weight_json['weight'][key]['date'])
    elif api_status_code==401:
        #Update Access Token using Refresh Token then repeat API request
        print(f'Refresh Required, Status Code{api_status_code}')
        refresh_status_code, refresh_json = refresh_request(refresh_token)
        if refresh_status_code == 200:
            access_token, refresh_token, userid = loadtokens(file_name)
            api_status_code, json_data = Weight_API(start_date, end_date, userid, access_token)
            for key in range(0,len(weight_json['weight'])):
                weight_values.append(weight_json['weight'][key]['weight']) 
                weight_dates.append(weight_json['weight'][key]['date'])
        else:
            print(refresh_json)
    else:
        print(f'Error Status Code: {api_status_code}')


weight_df = pd.DataFrame({'dateTime':weight_dates,'Weight':weight_values})
weight_df.to_csv('weight_df',index=False)


for index,row in dates.iterrows():
    start_date=str(row['Start'].date())
    end_date=str(row['End'].date())
    #Run API
    api_status_code, json_data = Step_API(start_date,end_date, userid, access_token)
    print(f'API Date Parameters: Start = {start_date}, End = {end_date}') 
    if api_status_code==200:
        #Temporarily store API data and append
        new_data = pd.DataFrame(json_data['activities-steps'])
        steps_df = pd.concat([steps_df,new_data],axis=0,ignore_index=True)
    elif api_status_code==401:
        #Update Access Token using Refresh Token then repeat API request
        print(f'Refresh Required, Status Code{api_status_code}')
        refresh_status_code, refresh_json = Refresh.refresh_request(refresh_token)
        if refresh_status_code == 200:
            access_token, refresh_token, userid = loadtokens(file_name)
            api_status_code, json_data = Step_API(start_date, end_date, userid, access_token)
            new_data = pd.DataFrame(json_data['activities-steps'])
            steps_df = pd.concat([steps_df,new_data],axis=0,ignore_index=True)
        else:
            print(refresh_json)
    else:
        print(f'Error Status Code: {api_status_code}')
print(steps_df)

steps_df.to_csv('steps_df',index=False)

