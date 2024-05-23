import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('my-table')

    for resource in event['resources']:
        item = {
            'resourceId': resource['InstanceId'],
            'resourceType': 'ec2',
            'tag': 'Custodian',
            'op': 'terminate',
            'days': 7
        }
        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }