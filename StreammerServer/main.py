#main file of the searcher.

"""This will be responsible to:
* launch the flask application that will stream the data
* launch all the thread's of processing and ensure they are alive
* receive notification of processing available for every camera
    * notification will come from a http post.
* every processing house will have an entrance and outgoing
* no database will be available
* processed pictures will be saved with their metadata
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from flask import Flask, Response
import shutil

from pathlib import Path

app = Flask(__name__)
@app.route("/")


def hello_world():
    return "<p>Hello, World!</p>"

def gather_img():
    while True:
        img = np.random.randint(0, 255, size=(1024, 600, 3), dtype=np.uint8)
        _, frame = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
        time.sleep(0.2)

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

@app.route("/face1")
def face_stream1():
    
    return Response(face_img('/dev/shm/camera/cam_1/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face2")
def face_stream2():
    return Response(face_img('/dev/shm/camera/cam_2/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face3")
def face_stream3():
    print("got to face 3")
    return Response(face_img('/dev/shm/camera/cam_3/stream/',face=3), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face4")
def face_stream4():
    return Response(face_img('/dev/shm/camera/cam_4/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face5")
def face_stream5():
    return Response(face_img('/dev/shm/camera/cam_5/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/test")
def mjpeg():
    return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(host='0.0.0.0', threaded=True)

if __name__ == "__main__":
    main()