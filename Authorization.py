import os
import requests
import base64
import secrets
import hashlib
import json

#Credentials Provided from Fitbit
ClientID = os.getenv('Fitbit_Client_ID')
Client_Secret = os.getenv('Fitbit_Client_Secret')


#Step 1: Create Code Challenge
#Code Verifier
Code_Verifier = secrets.token_urlsafe(64)
Code_Verifier_Hash = hashlib.sha256(Code_Verifier.encode()).digest()

#CodeChallenge
code_challenge = base64.urlsafe_b64encode(Code_Verifier_Hash).decode().rstrip('=')


#Step 2: Request Authorization
Fitbit_Authorize_URL = "https://www.fitbit.com/oauth2/authorize"
redirect_uri = "http://localhost"
scope_list = ['activity', 'heartrate', 'location', 'nutrition', 'oxygen_saturation', 'profile', 'respiratory_rate', 'settings', 'sleep', 'social', 'temperature', 'weight']
scope = "%20".join(scope_list)
authorization_url = f"{Fitbit_Authorize_URL}?client_id={ClientID}&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&scope={scope}&redirect_uri={redirect_uri}"


print(f"Authorize app via {authorization_url}")

#Step 3: Retreive Authorization Code
authorization_code = input("Enter Authorization Code")


#Step 4:
Token_URL = "https://api.fitbit.com/oauth2/token"

headers = {"Content-Type": "application/x-www-form-urlencoded", 
           "Authorization": f"Basic {base64.b64encode(f'{ClientID}:{Client_Secret}'.encode()).decode()}"}

payload = {'client_id': str(ClientID),
          'code': str(authorization_code),
          'code_verifier': str(Code_Verifier),
          'grant_type': 'authorization_code',
          'redirect_uri': redirect_uri}

token_response = requests.post(Token_URL,headers=headers,data=payload)

if token_response.status_code == 200:
    token_json = token_response.json()
    print('Response JSON', token_json)
    file_path = "../Credentials/accesstoken.json"
    with open(file_path, 'w') as json_file:
        json.dump(token_json, json_file, indent=2)
else: 
    print('Status Code', token_response.status_code)


