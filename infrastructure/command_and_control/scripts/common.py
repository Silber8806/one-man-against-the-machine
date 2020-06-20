#!/usr/bin/env python

import boto3

def get_account_id():
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    if (not isinstance(account_id, str) or account_id is None):
        account_id = None

    print("account id is:{}".format(account_id))

    return account_id

def get_boto_client():
    """ get a basic boto client """
    print("getting boto client...")
    client = boto3.client('ec2',region_name='us-east-1')
    return client

def get_command_and_control_reservations(client, account_id):
    """ get command and control class clients only"""
    print("returning instances associated with command and control")
    reservations = client.describe_instances(
        Filters=[
            {
                'Name':'iam-instance-profile.arn',
                'Values': [
                    'arn:aws:iam::{}:instance-profile/command_and_control'.format(account_id)
                ]
            }
        ]
    )['Reservations']

    return reservations