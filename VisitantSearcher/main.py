
"""This will be responsible to:
* launch as many searcher as configurable
* create the working folders
* configure the inotify to every folder
* get the events and deliver to the tasks
* stack the events if necessary
* control the flow of data if bogged down
"""
from Searcher import Searcher
from Common import util

import configparser

from time import sleep
import os
import sys
from pathlib import Path

from inotify_simple import INotify, flags





searchers = []
cameras = []
config = configparser.ConfigParser()
notifier = INotify()
watch_flags = flags.MODIFY | flags.DELETE_SELF
watch_party = []
alive = True
def main():
    while alive:
        for event in notifier.read(timeout=100):
            if event.name.startswith("met_"):
                tmp = event.name.split(".")
                pic_id = tmp[0].split("_")[1]
                camera_id = int(tmp[1])
                picture_name = "{}/img_{}.jpg".format(cameras[camera_id]["low_res_folder"],pic_id)
                searchers[camera_id].run(picture_name)
                break
    for searcher in searchers:
        del searcher
    for camera in cameras:
        del camera

        
if __name__ == "__main__":

    config.read("./assets/VisitantSearcher.conf")

    for section in config.sections():

        sec = config[section]
        if "debug" not in sec:
            sec["debug"] = "False"
        if ("found_folder" not in sec or
             "low_res_folder" not in sec or 
             "high_res_folder" not in sec or 
             "CamIP" not in sec or 
             "current_pan" not in sec or 
             "max_pan" not in sec or 
             "zero_pan"  not in sec or 
             "search_pan"  not in sec or 
             "go_to_pan"  not in sec or 
             "current_tilt"  not in sec or 
             "max_tilt"  not in sec or 
             "zero_tilt"  not in sec or 
             "search_tilt"  not in sec or 
             "go_to_tilt"  not in sec or
             "found_folder" not in sec or
             "stream_folder" not in sec or
             "max_head_size" not in sec or
             "min_head_size" not in sec 

            ):
            print("error in camera {}".format(section))
            continue
        go_home = False
        if "go_home" in sec:
            go_home = util.boolean(sec["go_home"])

        camera = {"low_res_folder": sec["low_res_folder"], 
                  "high_res_folder": sec["high_res_folder"],
                  "CamIP":sec["CamIP"]}
        cameras.append(camera)
        tmp  = Searcher.Searcher(
                                debug=util.boolean(sec["debug"]),
                                destination=sec["found_folder"],
                                stream=sec["stream_folder"],
                                IP=sec["CamIP"],
                                current_pan=int(sec["current_pan"]),
                                max_pan=int(sec["max_pan"]),
                                zero_pan=int(sec["zero_pan"]),
                                search_pan=util.boolean(sec["search_pan"]),
                                go_to_pan=int(sec["go_to_pan"]),
                                current_tilt=int(sec["current_tilt"]),
                                max_tilt=int(sec["max_tilt"]),
                                zero_tilt=int(sec["zero_tilt"]),
                                search_tilt=util.boolean(sec["search_tilt"]),
                                go_to_tilt=int(sec["go_to_tilt"]),
                                go_home=go_home,
                                min_head_size=float(sec["min_head_size"]),
                                max_head_size=float(sec["max_head_size"])
                                )
        searchers.append(tmp)
        wd = notifier.add_watch(sec["low_res_folder"], watch_flags)
        watch_party.append(wd)


try:
    main()
except KeyboardInterrupt:
    # terminate main thread
    alive = False

    print('Main interrupted! Exiting.')

    sys.exit()
        