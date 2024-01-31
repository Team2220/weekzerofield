#!/bin/bash

apt update
apt dist-upgrade -y
apt install git -y

sudo apt-get install python3.9 -y

mkdir /weekzerofield
cd /weekzerofield

git clone https://github.com/Team2220/weekzerofield.git
cd /server/
yes | python3 -m pip install -r weekzerofield/requirements.txt