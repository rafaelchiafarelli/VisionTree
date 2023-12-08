"""
The Searcher class 

"""

from Searcher.Move import Movement
from Searcher.Vision import Vision
from time import sleep

class Searcher():
    def __init__(self, 
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
        self.mover = Movement(IP)
        if self.go_to_pan != self.current_pan:
            self.move_to_pan()
        if self.go_to_tilt != self.current_tilt:
            self.move_to_tilt()
        
        self.visor = Vision(static_image_mode=True,
                            model_complexity=2,
                            enable_segmentation=True,
                            min_detection_confidence=0.5)
        

    def move_to_pan(self):
        while self.current_pan > self.go_to_pan:
            self.mover.MoveLeft()
            sleep(2)
            self.current_pan-=1
        while self.current_pan < self.go_to_pan:
            self.mover.MoveRight()
            sleep(2)
            self.current_pan+=1


    def move_to_tilt(self):
        while self.current_tilt > self.go_to_tilt:
            self.mover.MoveDown()
            sleep(2)
            self.current_tilt-=1
        while self.current_tilt < self.go_to_tilt:
            self.mover.MoveUp()
            sleep(2)
            self.current_tilt+=1

    def run(self, picture_name):
        """thread that will be running continuously"""
        
        print("get the picture {}".format(picture_name))
        self.visor.run(picture_name,destination="/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/")

        print("check for human bones (with mediapipe and pose-estimation)")

        print("check if there is a head")
        print("schedule a post to the server")
        print("move a litle bit to the side.")
