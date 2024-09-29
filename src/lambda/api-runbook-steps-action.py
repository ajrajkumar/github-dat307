import os
import boto3
import time
import json

boto3_session = boto3.session.Session()
region = boto3_session.region_name

# create a boto3 bedrock client
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

# agent_id = os.environ.get('AGENTID', 'JJ8DDCDQQ1')
agent_id = '2EOQS4ZE93'
#agent_alias_id = os.environ.get('AGENTALIASID', 'TZMOBGBUMZ')
agent_alias_id = '135OAPMTED'

def lambda_handler(event, context):
    print (event)
    query = event["alert"]
    sessionId = event["sessionId"]
    DBInstanceIdentifier= event["DBInstanceIdentifier"]
    alertType = event["alertType"]
    
    if alertType == "CPUUtilization":
        inputText=f"""
        The db_instance_identifier is {DBInstanceIdentifier}.  
        scale up the instance to the next available instance class using scale_up_i to fix the alert {alertType}.
        """
    elif alertType == "ReadWriteIOPS":
        inputText=f"""
        The db_instance_identifier is {DBInstanceIdentifier}.
        The percent_increase is 20.
        increase the IOPS provisioned on the given instance identifier using increase_i to fix the alert {alertType}.
        """
    if sessionId != "":
        response = bedrock_agent_runtime_client.invoke_agent(
            inputText=inputText,
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=sessionId,
            enableTrace=True,
            endSession=False
            #,
            #sessionState={
            #   "sessionAttributes": {
            #       "DBInstanceIdentifier": DBInstanceIdentifier
            #   }
            # }
           )
    else:
        response = bedrock_agent_runtime_client.invoke_agent(
            inputText=inputText,
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=sessionId,
            enableTrace=True,
            endSession=False
            #,sessionState={
            #   "sessionAttributes": {
            #       "DBInstanceIdentifier": DBInstanceIdentifier
            #   }
            # }
           )
    event_stream = response['completion']
    agent_answer = {"status": "Action completed successfully"}
    print (response)
    time.sleep (10)
    for event in event_stream:
        print (event)
        if 'chunk' in event:
            data = event['chunk']['bytes']
            print (f"Final answer ->\n{data.decode('utf8')}")
            agent_answer = data.decode('utf8')
            end_event_received = True

    return {
        'statusCode': 200,
        'body': json.dumps(agent_answer)
    }
