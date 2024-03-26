"""
The Searcher class 

"""

from Searcher.Move import Movement
from Searcher.Vision import Vision
import cv2
from time import sleep

mover = Movement(IP="192.168.15.7",
                        go_home=True,
                        max_steps=120,   
                        current_pan= 0,
                        max_pan = 120,
                        zero_pan = 0,
                        search_pan = True,
                        go_to_pan = 120,
                        current_tilt = 0,
                        max_tilt = 37,
                        zero_tilt = 0,
                        search_tilt = False,
                        go_to_tilt = 120)



    
mover.MoveLeft(False)


mover.MoveRight(False)


mover.MoveUp(False)                


mover.MoveDown(False)

while True:
    sleep(1)