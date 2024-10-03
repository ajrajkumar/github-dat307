import streamlit as st
from utils.apigw_handler import get_incidents, get_runbook, incident_remediate
from utils.init_session import reset_session
import pandas as pd
import json

def get_kpi(iconname, metricname, metricvalue):
    wch_colour_box = (0,204,102)
    wch_colour_font = (0,0,0)
    fontsize = 32
    valign = "left"
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.6.0/css/all.css" crossorigin="anonymous">'

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {metricvalue}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{metricname}</style></span></p>"""
    return lnk + htmlstr      

def app_page():
    incidents = get_incidents("pending")
    dfall = pd.DataFrame(incidents['Items'])   
    df = dfall.drop('alarmData', axis=1)
    df = df.drop('account_id', axis=1)
    # Get additional attributes from Alarm payload
    df['alert_type'] = dfall['alarmData'].str['name']
    df['db_instance'] = dfall['alarmData'].str['DBInstanceIdentifier']  
    
    eventCount = str(incidents['Count'])
    instanceCount =  str(df['db_instance'].nunique())
    alertTypeCount =  str(df['alert_type'].nunique())
    
    print("incident output")
    print(incidents)    
    st.set_page_config(page_title="DAT307-IDR: Amazon RDS Incidents", layout="wide")
    
    with st.sidebar:
        st.sidebar.image("image/idr_logo.png")        
        st.subheader("DAT307 - Build a Generative AI incident detection and response system powered by Amazon Aurora")
        st.divider()
        
        if st.button("Logout"):
            reset_session()
            st.rerun()
        
        st.sidebar.image("image/powered_by_aws.png",width=120)  


    st.title("Incidents")
    st.subheader("Metric Summary", divider=True)
    col1, col2, col3 = st.columns(3)
    #col1.metric(label="Total Pending Events", value=eventCount, delta_color="inverse")
    #col2.metric(label="Total Unique Instance", value=instanceCount)
    #col3.metric(label="Total Unique Alert Type", value=alertTypeCount)
    col1.markdown(get_kpi("fa-solid fa-circle-exclamation","Total Pending Events",eventCount), unsafe_allow_html=True)
    col2.markdown(get_kpi("fa-solid fa-server","Total Unique Instance",instanceCount), unsafe_allow_html=True)
    col3.markdown(get_kpi("fa-solid fa-bell","Total Unique Alert Type",alertTypeCount), unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    col4.markdown("#### Event Summary")
    col4.write("Here are the list of active incidents")
    col4.write("Please select an incident to process by clicking the first column of the row")
    
    print("Display table output")
    print(df)
    event = col4.dataframe(df,
                             on_select="rerun",
                             selection_mode="single-row",
                             hide_index=True,
                             column_config={
                             "alert_type": "Alert Type",
                             "pk": "Session ID",
                             "db_instance": "Database Instance",
                             "event_status": "Event Status"
                            },
                            column_order=("pk","db_instance","alert_type","event_status")
    )
    col4.markdown("#### Event Details")
    col4.divider()
    col5.markdown("#### User Action")
    col5.write("Here are the actions that requires manual user intervention")
    runbook_action = col5.button("Get Runbook")
    remediate_action = col5.button("Remediate Incident")
    col5.divider()
    rows = event['selection']['rows']
    pk = None
    description = None
    if len(rows) != 0:
        print(dfall)
        pk = dfall.iloc[rows[0]]['pk']
        description = dfall.iloc[rows[0]]['alarmData']['description']
        print(pk)
        col4.json(dfall.iloc[rows[0]].to_json(orient='records'))
        
 
    if runbook_action:
        if pk is None:
            col5.error("Please select an incident to get the runbook for the incident")
            return
        with col5.status("Retrieving incident runbook..."):
            runbook = get_runbook(pk,description)
            col5.markdown("***Runbook Instructions for " + pk + "***")
            col5.text_area("Runbook Instructions", runbook['runbook'],height=1000, label_visibility="hidden")

    if remediate_action:
        if pk is None:
            col5.error("Please select an incident to auto-remediate the incident")
            return
        with col5.status("Remediating incident..."):
            incident = incident_remediate(pk,description)
            col5.markdown("***Status of auto remediation for " + pk + "***")
            col5.info(incident['result'], icon="ℹ️")            