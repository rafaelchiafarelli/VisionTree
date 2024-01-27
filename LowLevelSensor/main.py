#main file of the searcher.

"""
This module is responsible to get all temperatures from the system, create an average and activate the control for it.

    *** control with steresys ***
        if ventilation do not have an effect in 30 minutes, will turn on a siren
        if siren and ventilation will not have an effect in 30 minutes, turn off the system ??


"""
import configparser
from Controller.Controller import Controller
from Actuator.Actuator import Actuator
from Sensor.Sensor import TempSensor
from time import sleep
import os
import sys

config = configparser.ConfigParser()
alive = True
global sensor
global actuator
global controller

def main():
    global alive

    while alive:
        sleep(2)
        temperature = sensor.Measure()
        print("temperature: {}".format(temperature))
        action = controller.Control(temperature)
        if action == 1:
            actuator.HighHigh()
        else:
            actuator.LowLow()


if __name__ == "__main__":


    config.read("./assets/LowLevelSensor.conf")
    
    id = 0
    sections = config.sections()
    if 'sensors' in sections:
        sensor = TempSensor(config["sensors"])
    

    if 'controller' in sections:
        controller = Controller(config["controller"])
    
    if 'actuator' in sections:
        actuator = Actuator(config['actuator'])
        actuator.begin()


try:
    main()
except :
    actuator.end()
    print('Main interrupted! Exiting.')
    
    sys.exit()
    