from threading import Thread
import os
import datetime
import shutil
from time import sleep
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
            with open("/home/rafael/workspace/VisionTree/records.txt", "a") as msg:
                self.current_data ="\"internet\":{},\"face_count\":{},\"disk_free\":{}\r\n".format(internet_data, face_data, disk_data)
                print(self.current_data)
                msg.write(self.current_data)
            sleep(1)


    def get_internet_data(self):
        start = datetime.datetime.now()
        ping = os.system("ping -c 1 www.google.com.br")
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S')
        response["status"] = ping
        return response
    
    def get_face_data(self):
        start = datetime.datetime.now()
        count=0
        for path in os.scandir("/home/rafael/storage"):
            if path.is_file():
                count+=1
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S')
        response["face_count"] = count
        return response
    
    def get_disk_usage(self):
        start = datetime.datetime.now()
        KB = 1024
        MB = 1024 * KB
        GB = 1024 * MB
        free = shutil.disk_usage("/").free / GB
        response = {}
        response["start"] = start.strftime('%Y-%m-%d %H:%M:%S')
        response["disk_free"] = free
        return response