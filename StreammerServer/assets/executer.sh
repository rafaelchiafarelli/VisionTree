#!/bin/bash

cd /home/rafael/workspace/VisionTree/
source venv/bin/activate
cd /home/rafael/workspace/VisionTree/StreammerServer
/home/rafael/workspace/VisionTree/venv/bin/python -m gunicorn -k gevent --workers 3 --bind unix:main.sock -m 007 wsgi:app