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
                 stream,
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
                 go_to_tilt,
                 go_home, 
                 configured_head_size
                   ):
        self.destination = destination
        self.stream = stream
        self.configured_head_size = configured_head_size
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
        self.go_home = go_home
        if self.max_pan < self.max_tilt:
            max_step = self.max_tilt    
        
        self.mover = Movement(IP=self.IP,
                              go_home=self.go_home,
                              max_steps=max_step,
                              current_pan= current_pan,
                              max_pan = max_pan,
                              zero_pan = zero_pan,
                              search_pan = search_pan,
                              go_to_pan = go_to_pan,
                              current_tilt = current_tilt,
                              max_tilt = max_tilt,
                              zero_tilt = zero_tilt,
                              search_tilt = search_tilt,
                              go_to_tilt = go_to_tilt )
        if self.go_to_pan != self.current_pan:
            self.move_to_pan()
        if self.go_to_tilt != self.current_tilt:
            self.move_to_tilt()
        
        self.debug = debug
        self.visor = Vision(debug=self.debug,
                            static_image_mode=True,
                            model_complexity=2,
                            enable_segmentation=True,
                            min_detection_confidence=0.5,
                            destination=self.destination)
        
    def __del__(self):
        del self.mover
        del self.visor
    
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

        has_head,pic_uuid, metadata = self.visor.search_body(picture_name)
        if has_head:
            print("there is a HEAD")
            """there is a HEAD
            if head is close to the center --> do nothing
            if it is to the lef --> move camera to the right
            if it is to the right --> move camera to the left
            do nothing if it is up or down
            """
            head_size = 0.5
            if metadata["right_ear"][0] > metadata["left_ear"][0]:
                head_size = metadata["right_ear"][0]-metadata["left_ear"][0]
            else:
                head_size = metadata["left_ear"][0]-metadata["right_ear"][0]

            
            if metadata["nose"][0] > 0.5 + head_size:

                self.mover.MoveLeft(False)
                
            if metadata["nose"][0] < 0.5 - head_size:

                self.mover.MoveRight(False)

                
            if metadata["nose"][1] < 0.5 + head_size:

                self.mover.MoveUp(False)                
            if metadata["nose"][1] > 0.5 - head_size:

                self.mover.MoveDown(False)


                
            self.SaveAndSend(picture_name,pic_uuid, metadata)
            self.visor.clean(pic_uuid)
        else:
            self.mover.continue_search()







    def SaveAndSend(self, picture_name, pic_uuid, metadata):
        """
        cut the face out of the picture
        save the picture in the stream folder
        """
        print("SaveAndSend")
        
        pic = cv2.imread(picture_name)
        pic_h,pic_w,_ = pic.shape
        #calculate the X inicial position
        nose_to_right_ear = metadata["right_ear"][0] - metadata["nose"][0]
        if nose_to_right_ear < 0:
            nose_to_right_ear = 0
        x = metadata["right_ear"][0]-nose_to_right_ear*4
        if x < 0:
            x = 0
        x = int(x * pic_w)
        # calculate the width
        if metadata["left_ear"] > metadata["right_ear"]:
            ear_to_ear = metadata["left_ear"][0] - metadata["right_ear"][0]
        else:
            ear_to_ear = metadata["right_ear"][0] - metadata["left_ear"][0]
        w = ear_to_ear*1.5
        w = int(w*pic_w)
        # calculate the Y inicial position
        eye_to_mounth_left = metadata["mounth_left"][1] - metadata["left_eye"][1]
        eye_to_mounth_right = metadata["mounth_right"][1] - metadata["right_eye"][1]
        eye_to_mounth = (eye_to_mounth_left + eye_to_mounth_right)/2
        y = ( (metadata["left_eye"][1] + metadata["right_eye"][1])/2 - eye_to_mounth*2)
        if y < 0:
            y = 0
        y = int(y*pic_h)
        # calculate the height 
        h  = eye_to_mounth * 4
        h = int(h * pic_h)
        head = pic[y:y+h,x:x+w]
        print("head: x: {} y: {} w:{} h:{}".format(x,y,w,h))
        print("pic shape w: {} h: {}".format(pic_w,pic_h))
        print("{}/{}.jpg".format(self.stream,pic_uuid))
        cv2.imwrite("{}/{}.jpg".format(self.stream,pic_uuid),head)
        if self.debug:
            cv2.imshow("head_pic", head) 
            # waits for user to press any key 
            # (this is necessary to avoid Python kernel form crashing) 
            cv2.waitKey(10) 


        