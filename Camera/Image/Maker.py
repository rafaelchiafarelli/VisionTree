"""Each image maker class will receive:
* the folder it must record (for both low and high)
* the address it should connect to receive the frames
    * The low resolution and the high resolution
* The picture format
* the picture max number
"""
from time import sleep
import cv2
import numpy as np
import os
from time import sleep
from threading import Thread
import datetime
import json

class ImageMaker:
    
    def __init__(self,name, low_res_folder, high_res_folder, max_pic, rtsp_low, rtsp_high):
        self.low_res_folder = low_res_folder
        self.high_res_folder = high_res_folder
        self.max_pic = max_pic
        self.rtsp_low = rtsp_low
        self.rtsp_high = rtsp_high
        self.name = name
        #don´t forget to use the Yoosee program to setup the password. The user will always be admin

        self.keep_alive = False

    def start(self):
        print("launch thread")
        self.keep_alive = True
        self.thread = Thread(target=self.th)
        self.thread.start()

    def stop(self):
        print("camera will join its thread")
        self.keep_alive = False
        self.thread.join()


    def th(self):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        low_res_cam = cv2.VideoCapture(self.rtsp_low, cv2.CAP_FFMPEG)
        high_res_cam = cv2.VideoCapture(self.rtsp_high, cv2.CAP_FFMPEG)

        ret,low_frame = low_res_cam.read()
        ret,high_frame = high_res_cam.read()

        id = 0
        
        while self.keep_alive:
            timestamp = datetime.datetime.now().timestamp() 
            ret,low_frame = low_res_cam.read()
            if ret is False:
                continue
            img_hsv = cv2.cvtColor(low_frame, cv2.COLOR_BGR2HSV)
            low_saturation = img_hsv[:, :, 1].mean()
            
            ret,high_frame = high_res_cam.read()
            if ret is False:
                continue
            img_hsv = cv2.cvtColor(high_frame, cv2.COLOR_BGR2HSV)
            high_saturation = img_hsv[:, :, 1].mean()

            if low_saturation > 10 and high_saturation > 10:
                self.save_frame(high_frame, self.high_res_folder, id, high_saturation, timestamp)
                self.save_frame(low_frame, self.low_res_folder, id, low_saturation, timestamp)
                id+=1
                if id > self.max_pic:
                    id = 0
        low_res_cam.release()
        high_res_cam.release()
                
    def save_frame(self, frame, folder, id, saturation,timestamp):
        img_path = '{}/img_{}.{}'.format(folder, id, "jpg")
        met_path = "{}/met_{}.{}".format(folder,id, self.name)
        os.remove(img_path)
        os.remove(met_path)
        cv2.imwrite(img_path, frame)
        with open(met_path, "w") as metadata:
            
            data = {"metadata":[{"timestamp":timestamp},
                    {"ID":id},
                    {"saturation":saturation}
                    ]}
            metadata.write(json.dumps(data,indent=1))
