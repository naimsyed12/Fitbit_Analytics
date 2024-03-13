import json
import requests
import os                                                                                           
from datetime import date, timedelta, datetime
import pandas as pd

#Import Access Token, Refresh Token, and Userid


def loadtokens(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data['access_token'], data['refresh_token'], data['user_id']


#Refresh Authorization using Refresh Token
def refresh_request(refresh_token):
    url = 'https://api.fitbit.com/oauth2/token'
    clientid = os.getenv('Fitbit_Client_ID')
    payload = {'grant_type':'refresh_token',
               'refresh_token':refresh_token,
               'client_id':str(clientid)}
    ref = requests.post(url,data=payload)
    if ref.status_code==200:
        with open('../Credentials/accesstoken.json','w') as json_file:
            json.dump(ref.json(), json_file, indent=2)
        print(f'Refreshed Access Token File, Status Code: {ref.status_code}')
    else: 
        print(f'Failed to Refresh Token, Status Code: {ref.status_code}')
    return ref.status_code, ref.json()

#Weight API Request using start/end dates
def Weight_API(start_date,end_date, userid, access_token):
    url = f'https://api.fitbit.com/1/user/{userid}/body/log/weight/date/{start_date}/{end_date}.json'
    header_dict = {'Authorization': f'Bearer {access_token}',
                   'Accept-Language':'en_US'}
    req = requests.get(url,headers=header_dict)       
    json_data=req.json()
    return req.status_code, json_data                                                   

#Steps API Request using start/end dates
def Step_API(start_date,end_date, userid, access_token):
    url = f'https://api.fitbit.com/1/user/{userid}/activities/steps/date/{start_date}/{end_date}.json'
    header_dict = {'Authorization': f'Bearer {access_token}',
                   'Accept-Language':'en_US'}
    req = requests.get(url,headers=header_dict)       
    json_data=req.json()
    return req.status_code, json_data                                                   
