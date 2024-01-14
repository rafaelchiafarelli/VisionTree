"""
The Searcher class 

"""

from Searcher.Move import Movement
from Searcher.Vision import Vision
import cv2
from time import sleep

mover = Movement(IP="192.168.0.228",
                        go_home=False,
                        max_steps=30,   
                        current_pan= 0,
                        max_pan = 0,
                        zero_pan = 0,
                        search_pan = True,
                        go_to_pan = 0,
                        current_tilt = 0,
                        max_tilt = 10,
                        zero_tilt = 0,
                        search_tilt = False,
                        go_to_tilt = 0)



    
mover.MoveLeft(False)


mover.MoveRight(False)


mover.MoveUp(False)                


mover.MoveDown(False)

