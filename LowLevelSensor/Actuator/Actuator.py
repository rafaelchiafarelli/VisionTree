import serial
from time import sleep
from threading import Thread
class Actuator:
    def __init__(self, conf):
        
        self.name = conf['name']
        self.baudrate = int(conf['baudrate'])
        self.timeout = 0.2 
        if 'timeout' in conf:
            self.timeout = float(conf['timeout'])
        self.state = 0
        
    
    def begin(self):
        print(self.name)
        print(self.baudrate)
        self.comm = serial.Serial(self.name, 
                                  self.baudrate,
                                  parity='N',
                                  stopbits=1,
                                  bytesize=8, 
                                  timeout=self.timeout)
        
        self.th = Thread(target=self.HartBeat)
        self.alive = True
        self.th.start()

    
    def end(self):
        self.alive = False
        self.th.join()
        self.comm.close()

    def HartBeat(self):
        while self.alive:
            if self.state == 1:
                self.comm.write(bytes(b'{r:002}\r\n'))
            else:
                self.comm.write(bytes(b'{r:000}\r\n'))
            sleep(0.1)
            
        

    def HighHigh(self):
        self.state = 1


    def LowLow(self):
        self.state = 0



