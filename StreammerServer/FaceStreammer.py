
import time
import matplotlib.pyplot as plt
import cv2
import os
from pathlib import Path
import numpy as np

def gather_img():
    while True:
        img = np.random.randint(0, 255, size=(1024, 600, 3), dtype=np.uint8)
        _, frame = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
        time.sleep(0.2)

def stream_img(path, id):
    while True:
        
        files = sorted(Path(path).iterdir(), key=lambda f: f.stat().st_mtime)
        for file in files:
            if ".jpg" in str(file):
                select_file = file
                break
        with open(select_file,"rb") as f:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + f.read() + b'\r\n')
            time.sleep(1/20)




def face_img(path, face = None):
    while True:
        time.sleep(1/20)
        files = sorted(Path(path).iterdir(), key=lambda f: f.stat().st_mtime)
        has_pic = False      
        for file in files:
            if ".jpg" in str(file):
                has_pic = True
                break
        if has_pic is not True:
            # create an image for the first time around, then keep the last
            img = np.random.randint(0, 255, size=(1024, 600, 3), dtype=np.uint8)
            _, frame = cv2.imencode('.jpg', img)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')            
        else:
            for file in files:
                if ".jpg" in str(file):
                    head = cv2.imread(str(file))
                    if head is None:
                        os.remove(file)
                        continue
                    img_gray = cv2.cvtColor(head, cv2.COLOR_BGR2GRAY)
                    hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
                    unsorted_hist = list()
                    sum= img_gray.size
                    for i,bin in enumerate(hist):
                        unsorted_hist.append(int(bin[0]))
                    
                    unsorted_hist.sort()
                    sorted_hist = unsorted_hist
                    resum = 0
                    bad_image = False
                    
                    for value in sorted_hist:
                        if value > sum/5:
                            bad_image = True
                            print("bad_image")
                            break
                        else:
                            resum+=value
                            if resum > sum - sum/3:
                                break

                    if bad_image is True:
                        try:
                            os.remove(file)
                        except:
                            file_name = os.path.basename(file)
                            print("Folder: {} and file:{} not found".format(path, file_name))

                        continue
                    else:
                        try:
                            with open(file,"rb") as f:
                                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + f.read() + b'\r\n')
                            file_name = os.path.basename(file)
                            #shutil.move(file, "/home/rafael/workspace/VisionTree/StreammerServer/assets/{}".format(file_name) )
                            os.remove(file)
                        except:
                            pass
                        break

def full_picture():
    cams =['/dev/shm/camera/cam_1/stream/',
           '/dev/shm/camera/cam_2/stream/',
           '/dev/shm/camera/cam_3/stream/',
           '/dev/shm/camera/cam_4/stream/']
    while True:
        select_file = []
        for cam in cams:
            files = sorted(Path(cam).iterdir(), key=lambda f: f.stat().st_mtime)
            for file in files:
                if ".jpg" in str(file):
                    select_file.append(file)
                    break

        img1 = cv2.imread(str(select_file[0]))
        img2 = cv2.imread(str(select_file[1]))
        img3 = cv2.imread(str(select_file[2]))
        img4 = cv2.imread(str(select_file[3]))
        vish = cv2.hconcat([img1, img2])
        visl = cv2.hconcat([img3, img4])
        vis = cv2.vconcat([vish,visl])
        
        select_file.clear()
        frame = vis.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        time.sleep(1/20)
