import streamlit as st
from utils.apigw_handler import get_incidents, get_runbook, incident_remediate
from utils.init_session import reset_session
import pandas as pd

def app_page():
    st.set_page_config(layout="wide")
    with st.sidebar:
        if st.button("Logout"):
            reset_session()
            st.rerun()
        
    st.title("Incidents")
    st.write("Here the list of active incidents")
    st.write("Please select an incident to process by clicking the first column of the row")
    incidents = get_incidents("pending")
    dfall = pd.DataFrame(incidents['Items'])
    df = dfall.drop('alarmData', axis=1)
    df = df.drop('account_id', axis=1)
    selection = st.dataframe(df, on_select="rerun", selection_mode="single-row", hide_index=True)
    runbook_action = st.button("Runbook")
    remediate_action = st.button("Remediate")
    rows = selection['selection']['rows']
    pk = None
    description = None
    if len(rows) != 0:
        pk = dfall.iloc[rows[0]]['pk']
        description = dfall.iloc[rows[0]]['alarmData']['description']
 
    if runbook_action:
        if pk is None:
            st.write("Please select an incident")
            return
        with st.spinner("Processing"):
            runbook = get_runbook(pk,description)
            st.write(runbook['runbook'])

    if remediate_action:
        if pk is None:
            st.write("Please select an incident")
            return
        with st.spinner("Processing"):
            incident = incident_remediate(pk,description)
            st.write(incident['result'])