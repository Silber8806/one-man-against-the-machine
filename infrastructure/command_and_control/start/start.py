#!/usr/bin/env python

import sys
import os
import boto3

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")

def get_boto_client():
    """ get a basic boto client """
    client = boto3.client('ec2',region_name='us-east-1')
    return client

def get_command_and_control_instances(client):
    """ get command and control class clients only"""
    return client.describe_instances(
        Filters=[
            {
                'Name':'iam-instance-profile.arn',
                'Values': [
                    'arn:aws:iam::{}:instance-profile/command_and_control'.format(ACCOUNT_ID)
                ]
            }
        ]
    )

def number_of_instances(reservations):
    """ get number of instances """
    if (len(reservations) != 1):
        print("too many reservations...existing...")
        sys.exit(1)
    try:
        instances = reservations['instances']
    except:
        print("reservations has no instances key...exiting")
        instances = []

    return len(instances)

def create_command_and_control_instance(client):
    if (os.path.exists('user_data.sh')):
        with open('user_data.sh','r') as user_data_script:
            user_data = user_data_script.read()
    else:
        print("Can't find user data file...exiting...")
        sys.exit(1)

    """ create a new ubuntu 18.04 command and control instance"""
    response = client.run_instances(
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='chriskottmyer',
        ImageId='ami-085925f297f89fce1',
        Monitoring={
            'Enabled': False
        },
        SecurityGroupIds=[
            'sg-77a3c002'
        ],
        SubnetId='subnet-bddb9f87',
        EbsOptimized=False,
        IamInstanceProfile={
            'Name':'command_and_control'
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'command and control'
                    }
                ]
            },
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key':'Name',
                        'Value': 'command and control'
                    }
                ]
            }
        ],
        UserData=user_data
    )
    return response

if __name__ == "__main__":
    client = get_boto_client()
    reservations = get_command_and_control_instances(client).get('Reservations',[])

    if (number_of_instances(reservations) == 0):
        print("no client found...spinning up...")
        response = create_command_and_control_instance(client)
        print("This is the response:")
        print(response)
    else:
        print("number of instances not 0...exiting")
        sys.exit(1)



