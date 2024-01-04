"""movement implementation of the ptz camera. 
This is a wrapper that will call the necessary commands to move the cameras.
One object for each camera
"""

from nodejs import node
from threading import Thread

from time import sleep
class Movement:
    def __init__(self, IP, go_home, max_steps):
        self.IP = IP
        self.moving = Thread(target=self.move)
        self.move_queue = []
        if go_home:
            self.GoHome(max_steps)
        self.alive = True
        self.moving.start()
    def __del__(self):
        self.alive = False
        self.moving.join(timeout=2000)

    def move(self):
        last_move = "NO_MOVE"
        while self.alive:
            print("is alive and queue is {}".format(self.move_queue))
            if len(self.move_queue) > 0:
                current_move =  self.move_queue.pop()
                if last_move != current_move:
                    node.run(['./Searcher/assets/ptz.js', self.IP, current_move], )
                    last_move = current_move
                    sleep(2)
            else:
                sleep(2)
            
    def GoHome(self,max_steps):
        print("GoHome Start")
        for i in range(0,max_steps):
            node.run(['./Searcher/assets/ptz.js', self.IP, "DWON"], )
            sleep(2)
            node.run(['./Searcher/assets/ptz.js', self.IP, "LEFT"], )
            sleep(2)
        print("GoHome End")


    def MoveUp(self, moves):
        if moves:
            print("moveup {}".format(moves))
            for i in range(0,moves):
                node.run(['./Searcher/assets/ptz.js', self.IP, "UP"], )
                sleep(2)
        else:
            self.move_queue.append("UP")

    def MoveDown(self, moves):
        if moves:
            print("movedown")
            for i in range(0,moves):
                node.run(['./Searcher/assets/ptz.js', self.IP, "DWON"], )
                sleep(2)
        else:
            self.move_queue.append("DWON")

    def MoveLeft(self, moves):
        if moves:
            print("moveleft")
            for i in range(0,moves):
                node.run(['./Searcher/assets/ptz.js', self.IP, "LEFT"], )
                sleep(2)
        else:
            self.move_queue.append("LEFT")
    
    def MoveRight(self, moves):
        print("moveright:{}".format(moves))
        if moves:
            for i in range(0,moves):
                node.run(['./Searcher/assets/ptz.js', self.IP, "RIGHT"], )
                sleep(2)
        else:
            self.move_queue.append("RIGHT")