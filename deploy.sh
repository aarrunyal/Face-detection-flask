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
pip3 install flask
pip3 install opencv-python
echo "******************Pip packages installed******************"

systemctl daemon-reload
systemctl restart gunicorn

systemctl disable face-detection.service
systemctl start face-detection.service
systemctl enable face-detection.service



systemctl restart nginx.service

systemctl status face-detection.service