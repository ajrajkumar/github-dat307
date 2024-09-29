import json
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Key
import streamlit as st
from streamlit_autorefresh import st_autorefresh


bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime', region_name="us-west-2")

def invoke_agent(query, session_id, agent_id, alias_id, enable_trace=False, session_state=None):
    end_session: bool = False
    if not session_state:
        session_state = {}

    # Invoke the agent API
    agent_response = bedrock_agent_runtime_client.invoke_agent(
        inputText=query,
        agentId=agent_id,
        agentAliasId=alias_id,
        sessionId=session_id,
        enableTrace=enable_trace,
        endSession=end_session,
        sessionState=session_state
    )

    event_stream = agent_response['completion']
    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                agent_answer = data.decode('utf8')
                return agent_answer
            elif 'trace' in event:
                pass  # Handle trace event if needed
            else:
                raise Exception("Unexpected event.", event)
    except Exception as e:
        raise Exception("Unexpected event.", e)

def get_pending_events():
    
    TABLE_NAME = "cwalerttable_v1"

    dynamodb_client = boto3.client('dynamodb', region_name="us-west-2")

    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table(TABLE_NAME)

    response = dynamodb_client.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='account_id = :account_id AND begins_with (event_status, :event_status)',
        ExpressionAttributeValues={
            ':account_id': {'S': '654654202661'},
            ':event_status': {'S': 'pending'}
        }
    )
    return response
	
def get_total_events(response):	
    
    pendingEventCount = str(response['Count'])
    print('Total pending events are: ' + pendingEventCount)
    return pendingEventCount

def get_event_details(response):
    json_df = pd.json_normalize(response['Items'])

    df = pd.DataFrame()

    df['account_id'] = json_df['account_id.S']
    df['event_status'] = json_df['event_status.S']
    df['event_details'] = json_df['event_details.S'] # test attribute
    #TODO: add the below attributes for the complete event details
    df['event_id'] = json_df['event_id.S'] if 'event_id.S' in json_df else None
    df['alert_name'] = json_df['alert_name.S'] if 'alert_name.S' in json_df else None
    df['alert_reason'] = json_df[
        'payload.M.detail.M.state.M.reason.S'] if 'payload.M.detail.M.state.M.reason.S' in json_df else None
    df['action_url'] = df.apply(lambda row: f'<button onclick="streamlit.setEventDetails(`{row["event_details"]}`)">Resolve</button>', axis=1)

    print(df)
    return df
    
def main():
    st.set_page_config(page_title="DAT307 - Build a Generative AI incident detection and response system powered by Amazon Aurora",
                       layout="wide",
                       page_icon=":elephant:")
    st.header("DAT307 - Build a Generative incident detection and response system powered by Amazon Aurora")
    
    # update every 1 min
    st_autorefresh(interval= 1 * 60 * 1000, key="dataframerefresh")
    res = get_pending_events()
    recordCount = str(get_total_events(res))
    event_df = get_event_details(res)

    if "selected_event_details" not in st.session_state:
        st.session_state["selected_event_details"] = ""

    st.write("### Pending Event Alerts")
    st.dataframe(event_df[['account_id', 'alert_name', 'event_id', 'event_status', 'alert_reason']])

    st.write("### Actions")
    for index, row in event_df.iterrows():
        if st.button(f"Resolve", key=f"resolve_{index}"):
            st.session_state["selected_event_details"] = row['event_details']

    if st.session_state["selected_event_details"]:
        st.write("### Chatbox")
        input_text = st.text_area("Incident Detection and Response Chat Interface", value=f"{st.session_state['selected_event_details']}",
                                  height=200)

        session_id = st.text_input("Session ID", value="session_1")
        agent_id = st.text_input("Agent ID", value="AY30ZW7EF6")
        alias_id = st.text_input("Alias ID", value="TSTALIASID")
        enable_trace = st.checkbox("Enable Trace", value=False)

        if st.button("Send to Bedrock"):
            response_text = invoke_agent(input_text, session_id, agent_id, alias_id, enable_trace)
            st.write("### Bedrock Agent Response")
            st.write(response_text)

if __name__ == '__main__':
    main()
