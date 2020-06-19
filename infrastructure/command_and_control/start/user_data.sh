#!/bin/bash

# this is a user data for command_and_control server

exec > /tmp/start_instance.log 2>&1

which pip3
pip_exists=$?

sudo apt update

if [[ "${pip_exists}" -ne "0" ]]
then
    echo "Installing pip3!"
    sudo apt install python3-pip
fi

which aws
aws_exists=$?

if [[ "${aws_exists}" -ne "0" ]]
then
    echo "Installing awscli!"
    sudo apt install awscli
fi


sudo pip3 install boto3
sudo pip3 install python-dotenv


