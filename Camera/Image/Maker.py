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
from matplotlib import pyplot as plt

class ImageMaker:
    
    def __init__(self,name, low_res_folder, high_res_folder, max_pic, rtsp_low, rtsp_high, max_error):
        
        self.low_res_folder = low_res_folder
        self.high_res_folder = high_res_folder
        self.max_pic = max_pic
        self.rtsp_low = rtsp_low
        self.rtsp_high = rtsp_high
        self.name = name
        self.max_error = max_error
        self.alive = False
        
        self.log("ID for this thread {}".format(self.name))
        self.keep_alive = False
    
    def log(self, data):
        print("ImageMaker[{}]:{}".format(self.name,data))
        
    def start(self):
        self.log("launch thread {}".format(self.name))
        self.keep_alive = True
        self.alive = True
        self.thread = Thread(target=self.th, args=(self.name,))
        self.thread.start()

    def stop(self):
        self.log("camera will join its thread")
        self.keep_alive = False
        self.thread.join()
    
    def restart(self):
        self.log("relaunch thread")
        self.stop()
        self.start()
        
    def isAlive(self):
        return self.alive

    def th(self, ID):
        self.log("running thread {}".format(ID))
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        #low_res_cam = cv2.VideoCapture(self.rtsp_low, cv2.CAP_FFMPEG)
        
        high_res_cam = cv2.VideoCapture(self.rtsp_high, cv2.CAP_FFMPEG)

        #ret,low_frame = low_res_cam.read()
        ret,high_frame = high_res_cam.read()
        
        id = 0
        err=0
        while self.keep_alive:
            timestamp = datetime.datetime.now()
        
            """ret,low_frame = low_res_cam.read()
            if ret is False:
                continue
            img_hsv = cv2.cvtColor(low_frame, cv2.COLOR_BGR2HSV)
            low_saturation = img_hsv[:, :, 1].mean()"""
            
            ret,high_frame = high_res_cam.read()
            
            if ret is False:
                err+=1
        
                if err > self.max_error:
                    err = 0
                    
                    break
                continue
            else:
                err = 0
            #cv2.imshow("pic{}".format(ID), cv2.cvtColor(high_frame,cv2.COLOR_BGR2RGB)) 
            # waits for user to press any key 
            # (this is necessary to avoid Python kernel form crashing) 
            #cv2.waitKey(10) 
            img_hsv = cv2.cvtColor(high_frame, cv2.COLOR_BGR2HSV)
            
            high_saturation = img_hsv[:, :, 1].mean()
            
            img_gray = cv2.cvtColor(high_frame, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
            unsorted_hist = list()
            sum= img_gray.size
            for i,bin in enumerate(hist):
                unsorted_hist.append(int(bin[0]))
                
                #self.log("value of position {} is {}".format(i,bin[0]))
            
            unsorted_hist.sort()
            sorted_hist = unsorted_hist
            resum = 0
            bad_image = False
            for value in sorted_hist:
                if value > sum/3:
                    #self.log("ID:{} too many of a single color".format(ID))
                    bad_image = True
                    break
                else:
                    resum+=value
                    if resum > sum - sum/3:
                        break

            if  high_saturation > 10 and bad_image is False: # and low_saturation > 10:
                self.save_frame(high_frame, self.high_res_folder, id, high_saturation, timestamp)

                #self.save_frame(low_frame, self.low_res_folder, id, low_saturation, timestamp)
                id+=1
                if id > self.max_pic:
                    id = 0
            sleep(0.1)

        #low_res_cam.release()
        high_res_cam.release()
        self.alive = False
                
    def save_frame(self, frame, folder, id, saturation,timestamp):
        img_path = '{}/img_{}.{}'.format(folder, id, "jpg")
        met_path = '{}/met_{}.{}'.format(folder, id, self.name)
        history_path = "../history_{}.met".format(self.name)
        
        os.remove(img_path)
        cv2.imwrite(img_path, frame)
        data = {}
        data = {}
        data["timestamp"] = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        data["ID"] = id
        data["saturation"] =saturation        
        with open(history_path, "a") as metadata:
            metadata.write("{}\r\n".format(json.dumps(data)))
            metadata.close()
        with open(met_path, "w") as met:
            met.write("{}".format(json.dumps(data)))
