#!/bin/bash

cd /home/rafael/workspace/VisionTree/
source venv/bin/activate
cd /home/rafael/workspace/VisionTree/StreammerServer
/home/rafael/workspace/VisionTree/venv/bin/python -m gunicorn -k gevent -w 4 -b :5000 main:app