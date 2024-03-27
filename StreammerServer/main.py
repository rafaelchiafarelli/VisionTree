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
from FaceStreammer import face_img, stream_img, gather_img, full_picture
from Status import Status
from Vote import Vote
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import cv2
import os
from flask import Flask, Response, render_template,send_from_directory, jsonify, request, redirect
from pathlib import Path
import datetime

app = Flask(__name__)
st = Status()
@app.route("/")
def landpage():
    return render_template('index.html')

@app.route("/static/<path:filename>")
def send_js(filename):
    return send_from_directory(filename, static_url_path='path')

@app.route("/face1")
def face_stream1():
    return Response(face_img('/dev/shm/camera/cam_1/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/face2")
def face_stream2():
    return Response(face_img('/dev/shm/camera/cam_2/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face3")
def face_stream3():

    return Response(face_img('/dev/shm/camera/cam_3/stream/',face=3), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/face4")
def face_stream4():
    return Response(face_img('/dev/shm/camera/cam_4/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/face5")
def face_stream5():
    return Response(face_img('/dev/shm/camera/cam_5/stream/'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam1")
def cam_stream1():
    return Response(stream_img('/dev/shm/camera/cam_1/high_res/',id=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam2")
def cam_stream2():
    return Response(stream_img('/dev/shm/camera/cam_2/high_res/',id=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam3")
def cam_stream3():

    return Response(stream_img('/dev/shm/camera/cam_3/high_res/',id=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam4")
def cam_stream4():
    return Response(stream_img('/dev/shm/camera/cam_4/high_res/',id=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam5")
def cam_stream5():
    return Response(stream_img('/dev/shm/camera/cam_5/high_res/',id=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed")
def full_pic():
    return Response(full_picture(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/restart/<int:cam>")
def mjpeg(cam):
    subprocess.run('/home/rafael/workspace/VisionTree/StreammerServer/assets/restarter.sh {}'.format(cam), shell=True, executable='/bin/bash')
    return {"restarting":True,"camera":cam}


@app.route("/statistics")
def statistics():

    d = st.status()
    return jsonify(d) 

@app.route('/vote/<int:vote>')
def voting(vote):
    """
    a vote goes from
    0 to 9
    """
    v = Vote(int(vote))
    
    return redirect("/")

@app.route("/message", methods=['POST'])
def message():
    raw = request.values.to_dict()
    print(raw)
    with open("/home/rafael/workspace/VisionTree/messages.txt", "a") as msg:
        now = datetime.datetime.now()
        line = "{},{},{},{}\r\n".format(raw['name'],raw['email'],raw['message'], now)
        print(line)
        msg.write(line)


    return redirect("/")

def main():
    app.run(host='0.0.0.0', threaded=True,debug=True)

if __name__ == "__main__":
    main()