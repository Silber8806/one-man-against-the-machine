#!/bin/bash

# this is a user data for command_and_control server

which pip3
pip_exists=$?

sudo apt update

if [[ "${pip_exists}" -ne "0" ]]
then
    echo "Installing pip3!"
    sudo apt install python3-pip
    echo "Finished installing pip3"
fi

which aws
aws_exists=$?

if [[ "${aws_exists}" -ne "0" ]]
then
    echo "Installing awscli!"
    sudo apt install awscli
    echo "Finished installing awscli"
fi