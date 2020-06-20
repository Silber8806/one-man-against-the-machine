#!/usr/bin/env python

import sys
import os
import boto3

from common import get_account_id, get_boto_client, get_command_and_control_reservations

def create_command_and_control_instance(client):
    """ create a new ubuntu 18.04 command and control instance"""
    if (os.path.exists('user_data.sh')):
        print("user data exists...")
        with open('user_data.sh','r') as user_data_script:
            user_data = user_data_script.read()
    else:
        print("Can't find user data file...exiting...")
        sys.exit(1)

    
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

    print("AWS API response:")
    print(response)

    return response

if __name__ == "__main__":
    print("starting command and control instance")
    account_id=get_account_id()

    if (account_id is None):
        print("account id does not exist...exiting")
        sys.exit(1)

    client = get_boto_client()
    reservations = get_command_and_control_reservations(client,account_id)

    instances = []
    for reservation in reservations:
        if 'Instances' in reservation:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])

    print("Found the following instances:")
    for instance in instances:
        print(instance)

    if (len(instances)==0):
        print("no client found...spinning up...")
        response = create_command_and_control_instance(client)
    elif(len(instances)==1):
        print("command and control instance already exists")
    elif (len(instances) > 1):
        print("too many command and control instances")
    else:
        print("number of instances not 0...exiting")
        sys.exit(1)



