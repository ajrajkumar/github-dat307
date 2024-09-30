import streamlit as st
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError
import requests

load_dotenv()
APIGWURL=os.getenv('APIGWURL')
APIGWSTAGE = os.getenv('APIGWSTAGE')
AWS_REGION=os.getenv('AWS_REGION')
       

def get_alerts():
    headers = {'Authorization': f"{st.session_state['token']}", 'Content-Type': 'application/json'}
    #print(headers)
    url = f'{APIGWURL}{APIGWSTAGE}/active-alerts'
    print (url)
    try:
       response = requests.get(url, headers = headers)
       response.raise_for_status()
       print(response.json())
       return response.json()
    except requests.exceptions.RequestException as e:
       print (f"Error in calling /alerts API: {e}")
       return None


def get_runbook(account_id,description):
    st.write(account_id)
    print("Calling the get_runbook")
    headers = {'Authorization': f"{st.session_state['token']}", 'Content-Type': 'application/json'}
    #print(headers)
    url = f'{APIGWURL}{APIGWSTAGE}/list-runbook-steps-alerts'
    print (url)
    try:
       response = requests.get(url, params={"query": description}, headers = headers)
       response.raise_for_status()
       print(response.json())
       st.write(response.json())
       return response.json()
    except requests.exceptions.RequestException as e:
       print (f"Error in calling /alerts API: {e}")
       return None

def alert_remediate(account_id,description):
    st.write(account_id)
    print("Calling the agent to take action")
    headers = {'Authorization': f"{st.session_state['token']}", 'Content-Type': 'application/json'}
    url = f'{APIGWURL}{APIGWSTAGE}/alert-runbook-steps-action'
    print (url)
    try:
       data = {'action':description}
       response = requests.post(url, headers = headers, json=data)
       response.raise_for_status()
       st.write(response.json())
    except requests.exceptions.RequestException as e:
       print (f"Error in calling /alerts API: {e}")
       return None   
    