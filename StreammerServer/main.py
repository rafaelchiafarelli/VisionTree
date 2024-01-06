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
        time.sleep(0.2)
        img = np.random.randint(0, 255, size=(128, 128, 3), dtype=np.uint8)
        _, frame = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

def face_img():
    while True:
        time.sleep(1/20)
        for file in sorted(Path('/dev/shm/camera/cam_1/stream/').iterdir(), key=lambda f: f.stat().st_mtime):
            if ".jpg" in str(file):
                head = cv2.imread(str(file))
                if head is None:
                    print("error reading image")
                    os.remove(file)
                    break
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
                        print("too many of a single color in the head")
                        bad_image = True
                        break
                    else:
                        resum+=value
                        if resum > sum - sum/3:
                            break

                if bad_image is True:
                    os.remove(file)
                    break
                else:
                    with open(file,"rb") as f:
                        print("file open")
                        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + f.read() + b'\r\n')
                    
                    file_name = os.path.basename(file)
                    #shutil.move(file, "/home/rafael/workspace/VisionTree/StreammerServer/assets/{}".format(file_name) )
                    break

@app.route("/face")
def face_stream():
    return Response(face_img(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/test")
def mjpeg():
    return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(host='0.0.0.0', threaded=True)

if __name__ == "__main__":
    main()