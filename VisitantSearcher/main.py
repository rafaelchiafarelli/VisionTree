
"""This will be responsible to:
* launch as many searcher as configurable
* create the working folders
* configure the inotify to every folder
* get the events and deliver to the tasks
* stack the events if necessary
* control the flow of data if bogged down
"""
from Searcher import Searcher
from Searcher.Move import Movement

import configparser

from time import sleep
import os
import sys
from pathlib import Path
searchers = []
config = configparser.ConfigParser()

def main():
    s1 = Searcher.Searcher(IP="192.168.0.165", current_pan=3,max_pan=10,zero_pan=1,search_pan=True,go_to_pan=3,current_tilt=4,max_tilt=30,zero_tilt=3,search_tilt=True,go_to_tilt=4);
    s1.run("/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/image.jpg")
    print("Hello World!")
    
    

if __name__ == "__main__":

    config.read("./assets/VisitantSearcher.conf")
    
    """
    for section in config.sections():

        sec = config[section]
        if "high_res_rtsp" not in sec or "low_res_rtsp" not in sec or "low_res_folder" not in sec or "high_res_folder" not in sec or "max_pic" not in sec:
            print("error in camera {}".format(section))
            continue

        tmp = Searcher.Searcher(current_pan=con)
        searchers.append(tmp)
    """
try:
    main()
except KeyboardInterrupt:
    # terminate main thread
    print('Main interrupted! Exiting.')

    sys.exit()
        