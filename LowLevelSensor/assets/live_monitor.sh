#!/bin/bash


while true
do
    cat /sys/class/hwmon/hwmon1/temp2_input
    sleep 1
done