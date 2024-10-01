import streamlit as st
from utils.apigw_handler import get_incidents, get_runbook, alert_remediate
from utils.init_session import reset_session

def app_page():
    st.set_page_config(layout="wide")
    with st.sidebar:
        if st.button("Logout"):
            reset_session()
            st.rerun()
        
    st.title("Incidents created")
    st.write("Here the list of active incidents")
    incidents = get_incidents("pending")
    user_table = incidents['Items']
    st.dataframe(user_table)
    colms =  st.columns((1, 2, 2,1, 1,1,1,2,2))
    fields = ['alarmData', 'event_details', 'sk', "event_status","pk", "account_id","Runbook","Remediate"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)

    for x, data in enumerate(user_table):
        col2, col3, col4, col5, col6,col7,col8,col9  = st.columns((1, 2, 2,1, 1,1,1,2))
        #col1, col2, col3, col4, col5, col6,col7,col8  = st.columns()
        #col1.write(x)  # index
        col2.write(data['alarmData'])  
        col3.write(data['event_details']) 
        col4.write(data['sk'])   
        col5.write(data['event_status'])  
        col6.write(data['pk'])   
        col7.write(data['account_id'])   
        button_runbook= col8.empty()  # create a placeholder
        button_remediate= col9.empty()  # create a placeholder
        runbook_action = button_runbook.button("Runbook", key=f"{data['account_id']}-rb",args=(data['account_id'],data['alarmData']['description'],), on_click=get_runbook)
        remediate_action = button_remediate.button("Remediate", key=f"{data['account_id']}-re", args=(data['account_id'],data['alarmData']['description']), on_click=alert_remediate)
