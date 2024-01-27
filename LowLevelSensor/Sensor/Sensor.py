import os
import shutil


class TempSensor:
    def __init__(self, config):
        self.SensorHome = config["SensorHome"]
        self.SensorList = config['SensorList'].split(',')
        self.SensorName = config['SensorName']
        dirs = ['/hwmon0','/hwmon1','/hwmon2']
        self.core_temp = []
        for dir in dirs:
            name = "{}{}/name".format(self.SensorHome,dir)
            if os.path.isfile(name):
                with open(name, 'r') as input:
                    dev_name = input.readline()
                    if 'coretemp' in dev_name :
                        self.core_temp.append(dir)
        
    
    def Measure(self):
        acc = 0
        error = False
        for core in self.core_temp:
            for sensor in self.SensorList:
                filename = "{}{}/{}".format(self.SensorHome,core,sensor)
                if os.path.isfile(filename):
                    with open(filename,'r') as s:
                        acc+=int(s.readline())
                        s.close()
                else:
                    error=True
                    break
        if not error:
            avg = acc/(2*len(self.SensorList))
            return avg
        return -1
                