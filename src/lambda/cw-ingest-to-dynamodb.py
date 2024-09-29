import json
import logging
import os
import boto3
import uuid

def lambda_handler(event, context):
    # TODO implement
    print (event)
    print (context)
    dynamodb = boto3.client('dynamodb')
    tableName = 'cwalerttable_v1'
    metricStat = {}
    id = 'xyz'
    for x in event.get('alarmData').get('configuration').get('metrics'):
        metricStat = x.get('metricStat')
        if  metricStat:
            break
    
    event_details = '{} Alarm triggered for DBInstanceIdentifier {}, Reason {}'.format( 
        metricStat.get('metric').get('name'),
        metricStat.get('metric').get('dimensions').get('DBInstanceIdentifier'),
        event.get('alarmData').get('state').get('reason').split('.')[0]
        )
    item = {'account_id':{'S': uuid.uuid4().hex },
            'event_status':{'S': 'pending'},
            'event_details': {'S': event_details},
            'alarmData': {'M': {
                                'alarmName': {'S': event.get('alarmData').get('alarmName')},
                                'reason': {'S': event.get('alarmData').get('state').get('reason')},
                                'namespace': {'S': metricStat.get('metric').get('namespace')},
                                'name': {'S': metricStat.get('metric').get('name')},
                                'DBInstanceIdentifier': {'S': metricStat.get('metric').get('dimensions').get('DBInstanceIdentifier')}
                            }
                        } }
    response = dynamodb.put_item(TableName=tableName, Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

