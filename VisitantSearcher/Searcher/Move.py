"""movement implementation of the ptz camera. 
This is a wrapper that will call the necessary commands to move the cameras.
One object for each camera
"""

import requests


from threading import Thread

from time import sleep
class Movement:
    def __init__(self, IP, 
                go_home, 
                max_steps, 
                current_pan,
                max_pan,
                zero_pan,
                search_pan,
                go_to_pan,
                current_tilt,
                max_tilt,
                zero_tilt,
                search_tilt,
                go_to_tilt ):
        self.IP = IP
        self.moving = Thread(target=self.move)
        self.move_x_queue = []
        self.move_y_queue = []

        self.xml = "<s:Envelope xmlns:s=\"http://www.w3.org/2003/05/soap-envelope\"><s:Body xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><ContinuousMove xmlns=\"http://www.onvif.org/ver20/ptz/wsdl\"><ProfileToken>IPCProfilesToken0</ProfileToken><Velocity><PanTilt x=\"{}\" y=\"{}\" xmlns=\"http://www.onvif.org/ver10/schema\"/></Velocity></ContinuousMove></s:Body></s:Envelope>"
        self.headers = {'Content-Type': 'application/xml'} # set what your server accepts
        self.url = 'http://{}:5000/onvif/deviceio_service'
        self.max_steps = max_steps
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
        self.go_home = go_home            

        self.alive = True
        self.moving.start()

    def Stop(self):
        self.alive = False
        self.moving.join(timeout=2000)        


    def __del__(self):
        self.alive = False
        self.moving.join(timeout=2000)

    def move(self):
        last_x_move = "NO_MOVE"
        last_y_move = "NO_MOVE"
        if self.alive:
            if self.go_home:
                self.GoHome()
            self.move_to_pan()
            self.move_to_tilt()
           

        while self.alive:
            
            if len(self.move_x_queue) > 0:
                current_x_move =  self.move_x_queue.pop()
                if last_x_move != current_x_move:
                    if current_x_move == "LEFT":
                        print("left decrease")
                        if self.zero_pan < self.current_pan:
                            requests.post(self.url.format(self.IP), data=self.xml.format(1,0), headers=self.headers)
                            self.current_pan-=1
                    elif current_x_move == "RIGHT":
                        print("right increases")
                        if self.max_pan > self.current_pan:
                            requests.post(self.url.format(self.IP), data=self.xml.format(-1,0), headers=self.headers)
                            self.current_pan+=1
                    

                    last_x_move = current_x_move
                    sleep(1)
            else:
                last_x_move = "NO_MOVE"

            if len(self.move_y_queue) > 0:
                current_y_move =  self.move_y_queue.pop()
                if last_y_move != current_y_move:
                    if current_y_move == "DWON":
                        print("dwon decrease")  
                        if self.zero_tilt < self.current_tilt:
                            requests.post(self.url.format(self.IP), data=self.xml.format(0,1), headers=self.headers)
                            self.current_tilt-=1
                    elif current_y_move == "UP":
                        print("up increases")                  
                        if self.max_tilt > self.current_tilt:
                            requests.post(self.url.format(self.IP), data=self.xml.format(0,-1), headers=self.headers)
                            self.current_tilt+=1
                    last_y_move = current_y_move
                    sleep(1)
            else:
                last_y_move = "NO_MOVE"
            sleep(0.1)
    def continue_search(self):
        
        pass

    def GoHome(self):
        print("GoHome Start")
        for i in range(0,self.max_steps):
            requests.post(self.url.format(self.IP), data=self.xml.format(0,1), headers=self.headers)
            sleep(1)
            requests.post(self.url.format(self.IP), data=self.xml.format(1,0), headers=self.headers)
            sleep(1)
            if self.alive is not True:
                break
        print("GoHome End")


    def MoveUp(self, moves):
        print("moveup moves:{}".format(moves))
        if moves:
        
            for i in range(0,moves):
                requests.post(self.url.format(self.IP), data=self.xml.format(0,-1), headers=self.headers)
                sleep(1)
        else:
            self.move_y_queue.append("UP")

    def MoveDown(self, moves):
        
        if moves:
            
            for i in range(0,moves):
                requests.post(self.url.format(self.IP), data=self.xml.format(0,1), headers=self.headers)
                sleep(1)
        else:
            self.move_y_queue.append("DWON")

    def MoveLeft(self, moves):
        print("moveleft moves:{}".format(moves))
        if moves:
            
            for i in range(0,moves):
                requests.post(self.url.format(self.IP), data=self.xml.format(1,0), headers=self.headers)
                sleep(1)
        else:
            self.move_x_queue.append("LEFT")
    
    def MoveRight(self, moves):
        print("moveright:{}".format(moves))
        if moves:
            for i in range(0,moves):
                requests.post(self.url.format(self.IP), data=self.xml.format(-1,0), headers=self.headers)
                sleep(1)
        else:
            self.move_x_queue.append("RIGHT")

    
    def move_to_pan(self):
        if self.current_pan > self.go_to_pan:
            self.MoveLeft(self.current_pan-self.go_to_pan)

        if self.current_pan < self.go_to_pan:
            self.MoveRight(self.go_to_pan-self.current_pan)
        self.current_pan = self.go_to_pan



    def move_to_tilt(self):
        if self.current_tilt > self.go_to_tilt:
            self.MoveDown(self.current_tilt - self.go_to_tilt)

        if self.current_tilt < self.go_to_tilt:
            self.MoveUp(self.go_to_tilt - self.current_tilt)
        self.current_tilt = self.go_to_tilt            