#main file of the searcher.

"""
This will be responsible to:
* create all the folders pertinent to this process (in dev/shm)
    * one cam_# for each camera
    * one cam_#/low_res 
    * one cam_#/high_res

* launch one thread per camera available
* establish the connection to the camera
    * low res
    * high res
* ensure there is a frame available
* store this into the out folder with the number
    * the format is still not defined. 
    * the format is going to be the one that is faster
    * there is no reason to save it in JPG if there will be more processing required
    * example: /dev/shm/cam_1/low_res/img_0.png 
    * the amount of picture that is saved is configurable
        * minimum is 5 maximum is 50
* manage deletion of the new files.        
"""
import configparser
from Image import Maker
from time import sleep
import os
import sys
from pathlib import Path
from shutil import copy, chown
import subprocess
cameras = []
config = configparser.ConfigParser()
alive = True
dead = False

def create_folder(full_path,id, max_pic):
    path = Path(full_path)
    path.mkdir(parents=True, exist_ok=True)
    chown(path=path,user="rafael",group="rafael")
    for i in range(0, int(max_pic)+1):
        copy("./assets/img.jpg", "{}/img_{}.jpg".format(full_path, i))
        copy("./assets/met", "{}/met_{}.{}".format(full_path,i,id))


if __name__ == "__main__":
    id = sys.argv[1]
    config.read("./assets/camera{}.conf".format(id))
    
    for section in config.sections():
        
        sec = config[section]
        print(sec)
        if "high_res_rtsp" not in sec or "low_res_rtsp" not in sec or "low_res_folder" not in sec or "high_res_folder" not in sec or "max_pic" not in sec or "max_error" not in sec:
            print("error in camera {}".format(section))
            continue

        create_folder(sec["low_res_folder"],str(id), sec["max_pic"])
        create_folder(sec["high_res_folder"],str(id), sec["max_pic"])
        create_folder(sec["found_folder"],str(id), 0)
        create_folder(sec["stream_folder"],str(id), 0)
        conf = {'id':str(id),
         'low_res_folder':sec["low_res_folder"],
         'high_res_folder':sec["high_res_folder"],
         'max_pic':int(sec["max_pic"]),
         'low_res_rtsp':sec["low_res_rtsp"],
         'high_res_rtsp':sec["high_res_rtsp"],
         'max_error':int(sec["max_error"])
         }
        print(conf)


    try:
        camera = Maker.ImageMaker(name = conf["id"],
                                low_res_folder=conf["low_res_folder"],
                                high_res_folder=conf["high_res_folder"],
                                max_pic=conf["max_pic"],
                                rtsp_low=conf["low_res_rtsp"],
                                rtsp_high=conf["high_res_rtsp"],
                                max_error=conf["max_error"])
        camera.start()
        while alive:
            sleep(1)

    except :
        camera.stop()
        alive = False
        count=0
        while camera.isAlive() and count<5:
            sleep(1)
            count+=1
        sys.exit()
        