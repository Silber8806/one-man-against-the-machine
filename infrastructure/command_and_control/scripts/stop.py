#!/usr/bin/env python

import sys
import boto3

from common import get_account_id, get_boto_client, get_command_and_control_reservations

if __name__ == "__main__":
    print("starting command and control instance")
    account_id = get_account_id()

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

    print("deleting the following ids:")
    for instance in instances:
        print(instance)

    if (instances):
        response = client.terminate_instances(InstanceIds=instances)
        print("this is the current response:")
        print(response)
    else:
        print("no instances found...")