#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 20:06:51 2019

@author: jnunez
"""

from serial import Serial
import TMCL
import threading

## serial-address as set on the TMCM module.
MODULE_ADDRESS = 1
COM_PORT = 'COM3'

    
def angle_to_steps(angle):
    return int(461900*angle/360)

class Turntable (threading.Thread):

    def __init__(self):   
        threading.Thread.__init__(self)
        ## Open the serial port presented by your rs485 adapter
        self.serial_port = Serial(COM_PORT, 9600)
        #serial_port = Serial("/dev/ttyACM0", 9600)
        print('Using port...', self.serial_port.name)
    
        ## Create a Bus instance using the open serial port
        self.bus = TMCL.Bus(self.serial_port)
    
        ## Get the motor
        self.motor = self.bus.get_motor(MODULE_ADDRESS)    
   
    def setparams(self, maxspeed=10, maxaccel=500):
  # ajustamos parámetros
        self.motor.axis.max_positioning_speed = maxspeed
        self.motor.axis.max_accelleration = maxaccel
        
        # Ponemos referencia posiciones
        self.motor.axis.actual_position = 0       
          
    def start(self,angle):
        self.motor.move_absolute(angle_to_steps(angle))
        
    def end(self):
        self.serial_port.close()
        


      
        

#t = time.process_time()
#while motor.reference_search(motor.RFS_STATUS)!=motor.RFS_STATUS:
#    print (motor.reference_search(motor.RFS_STATUS))
#    elapsed_time = time.process_time() - t
#    time.sleep(1)
#print(elapsed_time)





