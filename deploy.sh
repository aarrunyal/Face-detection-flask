#!/bin/bash

echo "******************Pulling from the github******************"
git pull origin main
echo "******************Pulled from the github******************"

echo "******************Removing env file******************"
rm -rf env
echo "******************Removed env file******************"

echo "******************Creating new env ******************"
python3 -m venv env
echo "******************New env created ******************"


echo "******************Pip package installation ongoing******************"
pip3 install wheel
pip3 install gunicorn
pip3 install opencv-python
pip3 install flask
echo "******************Pip package installation ongoing******************"

if (systemctl -q is-active face-detection.service)
    then
    systemctl restart face-detection.service
    echo "******************Restarting system service******************"
fi
