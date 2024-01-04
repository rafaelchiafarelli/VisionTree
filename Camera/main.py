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
from shutil import copy
cameras = []
config = configparser.ConfigParser()

def main():
    while True:
        sleep(1)

def create_folder(full_path,id, max_pic):
    path = Path(full_path)
    path.mkdir(parents=True, exist_ok=True)
    for i in range(0, int(max_pic)+1):
        copy("./assets/img.jpg", "{}/img_{}.jpg".format(full_path, i))
        copy("./assets/met", "{}/met_{}.{}".format(full_path,i,id))


if __name__ == "__main__":

    config.read("./assets/camera.conf")
    
    id = 0
    for section in config.sections():

        sec = config[section]
        if "high_res_rtsp" not in sec or "low_res_rtsp" not in sec or "low_res_folder" not in sec or "high_res_folder" not in sec or "max_pic" not in sec:
            print("error in camera {}".format(section))
            continue

        create_folder(sec["low_res_folder"],str(id), sec["max_pic"])
        create_folder(sec["high_res_folder"],str(id), sec["max_pic"])
        create_folder(sec["found_folder"],str(id), 0)
        create_folder(sec["stream_folder"],str(id), 0)
        
        tmp = Maker.ImageMaker(str(id),sec["low_res_folder"],sec["high_res_folder"],int(sec["max_pic"]),sec["low_res_rtsp"], sec["high_res_rtsp"])
        tmp.start()
        cameras.append(tmp)
        id+=1

try:
    main()
except KeyboardInterrupt:
    # terminate main thread
    print('Main interrupted! Exiting.')
    for camera in cameras:
        camera.stop()
    sys.exit()
    