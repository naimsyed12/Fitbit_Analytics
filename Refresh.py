import requests
import os
import json



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