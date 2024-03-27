#!/bin/bash

cd /home/rafael/workspace/VisionTree/
/bin/touch history_$1.met
source venv/bin/activate
cd /home/rafael/workspace/VisionTree/Camera
python main.py "$1"