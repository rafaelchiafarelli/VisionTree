import json
from threading import Thread
import os
import datetime
import shutil
from time import sleep
from shutil import copy, chown
class Status():
    def __init__(self) -> None:
        self.alive = True
        with open("/home/rafael/workspace/VisionTree/records.txt", 'rb') as file:
            try:
                file.seek(-2,os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2,os.SEEK_CUR)
            except OSError:
                    file.seek(0)
            self.current_data = file.readline().decode()
            file.close()
            if len(self.current_data) == 0:
                self.current_data = "{\"internet\":{\"start\":00,\"status\":-1}, \"face_count\":{\"start\":00,\"face_count\":0},\"disk_free\":{\"start\":00,\"disk_free\":0}}"

        self.th = Thread(target=self.DataGatter)
        self.th.start()

    def status(self):
        return self.current_data
    

    def  DataGatter(self):
        
        while self.alive is True:
            internet_data = self.get_internet_data()
            face_data = self.get_face_data()
            disk_data = self.get_disk_usage()
            metadata = self.get_cam_data()
            with open("/home/rafael/workspace/VisionTree/records.txt", "a") as msg:
                self.current_data ="\"internet\":{},\"face_count\":{},\"disk_free\":{}, \"cameras\":{}\r\n".format(internet_data, face_data, disk_data,metadata)
                msg.write(self.current_data)
            sleep(1)


    def get_internet_data(self):
        start = datetime.datetime.now()
        ping = os.system("ping -c 1 www.google.com.br > /dev/null")
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S.%f')
        response["status"] = ping
        return response
    
    def get_face_data(self):
        start = datetime.datetime.now()
        count=0
        for path in os.scandir("/home/rafael/storage"):
            if path.is_file():
                count+=1
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S.%f')
        response["face_count"] = count
        return response
    
    def get_disk_usage(self):
        start = datetime.datetime.now()
        KB = 1024
        MB = 1024 * KB
        GB = 1024 * MB
        free = shutil.disk_usage("/").free / GB
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S.%f')
        response["disk_free"] = free
        return response
    def get_cam_data(self):
        start = datetime.datetime.now()
        metadata = []
        for cam in range(1,5):
            with open("/home/rafael/workspace/VisionTree/history_{}.met".format(cam), 'rb') as file:
                try:
                    file.seek(-2,os.SEEK_END)
                    while file.read(1) != b'\n':
                        file.seek(-2,os.SEEK_CUR)
                except OSError:
                        file.seek(0)
                data = file.readline().decode().split("\r")[0]
                raw = json.loads(data)
                raw["picname"] = "./static/temp/cam_{}_pic_{}.jpg".format(cam,raw["ID"])
                copy("/dev/shm/camera/cam_{}/high_res/img_{}.jpg".format(cam,raw["ID"]), 
                     raw["picname"])
                
                metadata.append(raw)
                file.close()
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S.%f')
        response["metadata"] = metadata
        
        return response