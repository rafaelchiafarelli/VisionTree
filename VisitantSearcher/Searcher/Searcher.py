"""
The Searcher class 

"""

from Searcher.Move import Movement
from Searcher.Vision import Vision
import cv2
from time import sleep

class Searcher():
    def __init__(self,
                 debug, 
                 destination,
                 IP,
                 current_pan, 
                 max_pan, 
                 zero_pan,
                 search_pan, 
                 go_to_pan,
                 current_tilt, 
                 max_tilt, 
                 zero_tilt, 
                 search_tilt, 
                 go_to_tilt
                   ):
        self.destination = destination
        self.IP = IP
        self.current_pan = current_pan
        self.max_pan = max_pan
        self.zero_pan = zero_pan
        self.search_pan = search_pan
        self.go_to_pan = go_to_pan
        self.current_tilt = current_tilt
        self.max_tilt = max_tilt
        self.zero_tilt = zero_tilt
        self.search_tilt = search_tilt
        self.go_to_tilt = go_to_tilt 
        max_step = self.max_pan
        if self.max_pan < self.max_tilt:
            max_step = self.max_tilt    
        
        self.mover = Movement(self.IP,True,max_step)
        if self.go_to_pan != self.current_pan:
            self.move_to_pan()
        if self.go_to_tilt != self.current_tilt:
            self.move_to_tilt()
        self.debug = debug
        self.visor = Vision(debug=self.debug,
                            static_image_mode=True,
                            model_complexity=2,
                            enable_segmentation=True,
                            min_detection_confidence=0.5)
        

    def move_to_pan(self):
        print("move to pan from: {} to: {}".format(self.current_pan, self.go_to_pan))
        if self.current_pan > self.go_to_pan:
            self.mover.MoveLeft(self.current_pan-self.go_to_pan)

        if self.current_pan < self.go_to_pan:
            self.mover.MoveRight(self.go_to_pan-self.current_pan)
        self.current_pan = self.go_to_pan



    def move_to_tilt(self):
        print("move to tilt from: {} to: {}".format(self.current_tilt, self.go_to_tilt))
        if self.current_tilt > self.go_to_tilt:
            self.mover.MoveDown(self.current_tilt - self.go_to_tilt)

        if self.current_tilt < self.go_to_tilt:
            self.mover.MoveUp(self.go_to_tilt - self.current_tilt)
        self.current_tilt = self.go_to_tilt


    def run(self, picture_name):
        """thread that will be running 
        
        print("get the picture {}".format(picture_name))
        print("check for human bones (with mediapipe and pose-estimation)")
        continuously"""

        pic_uuid, metadata = self.visor.search_body(picture_name,"/home/rafael/person_found")
        if pic_uuid:
            print("there is a HEAD")
            """there is a HEAD
            if head is close to the center --> do nothing
            if it is to the lef --> move camera to the right
            if it is to the right --> move camera to the left
            do nothing if it is up or down
            """
            head_size = (metadata["right_ear"][0]-metadata["left_ear"][0])
            print("head_size {}".format(head_size))
            if metadata["nose"][0] > 0.5 + head_size:
                self.mover.MoveRight(False)
                return
            if metadata["nose"][0] < 0.5 - head_size:
                self.mover.MoveLeft(False)
                return
            """distance between the mouth and the ear"""
            
            ear_to_mouth = (metadata["mouth_left"][1]+metadata["mouth_right"][1]/2) - (metadata["left_ear"][1] + metadata["right_ear"][1])/2 
            """head_area = [x, y, witdth, height]"""
            print("ear_to_mouth {}".format(ear_to_mouth))

            head_area = [metadata["nose"][0] - head_size/2 ,metadata["nose"][1] - 3 * ear_to_mouth, head_size, ear_to_mouth * 5]

            print("head_area {}".format(head_area))
                

        """print(landmarks)
        if ( "nose" in landmarks and
            "left_eye_inner" in landmarks and
            "left_eye_" in landmarks and
            "left_eye_outer" in landmarks and
            "right_eye_inner" in landmarks and
            "right_eye" in landmarks and
            "right_eye_outer" in landmarks and
            "mounth_left" in landmarks and
            "mounth_right" in landmarks
            ):
            print("there is a head -- separate this part in the bigger image and show it to the user")




        print("check if there is a head")
        print("schedule a post to the server")
        print("move a litle bit to the side.")
        """    