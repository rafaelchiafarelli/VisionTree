import serial
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
        self.comm = serial.Serial(self.name, 
                                  self.baudrate,
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE,
                                  bytesize=serial.EIGHTBITS, 
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
                self.comm.write(bytes(b'{a:002}\n'))
                
            else:
                self.comm.write(bytes(b'{a:000}\n'))
            self.comm.flush()
            
            msg = self.comm.readline()
            

    def HighHigh(self):
        self.state = 1


    def LowLow(self):
        self.state = 0



