import json
import requests
import os                                                                                           
import Refresh
from datetime import date
import pandas as pd


file_name = '../Credentials/accesstoken.json'                                                                                         

#Load Access/Refresh Tokens and Userid to use for API Requests/Refresh 
def loadtokens(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data['access_token'], data['refresh_token'], data['user_id']

access_token, refresh_token, userid = loadtokens(file_name)

#Steps API Request
def API_Req(start_date,end_date):
    url = f'https://api.fitbit.com/1/user/{userid}/activities/steps/date/{start_date}/{end_date}.json'
    header_dict = {'Authorization': f'Bearer {access_token}',
                   'Accept-Language':'en_US'}
    req = requests.get(url,headers=header_dict)       
    json_data=req.json()
    return req.status_code, json_data                                                   

     

#Create Date Range DataFrame for iteration
start_dates = pd.date_range(start=date(2019,6,1),end=date(2024,2,29),freq='MS')
end_dates = pd.date_range(start=date(2019,6,1),end=date(2024,2,29),freq='M')
dates=pd.DataFrame({'Start':start_dates,'End':end_dates})

#Empty DataFrame to append with steps data throughout loop
steps_df = pd.DataFrame()

#Iterate through date range to retrieve, parse, and store API data
for index,row in dates.iterrows():
    start_date=str(row['Start'].date())
    end_date=str(row['End'].date())
    #Run API
    api_status_code, json_data = API_Req(start_date,end_date)
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
            api_status_code, json_data = API_Req(start_date, end_date)
            new_data = pd.DataFrame(json_data['activities-steps'])
            steps_df = pd.concat([steps_df,new_data],axis=0,ignore_index=True)
        else:
            print(refresh_json)
    else:
        print(f'Error Status Code: {api_status_code}')
print(steps_df)

steps_df.to_csv('steps_df',index=False)


