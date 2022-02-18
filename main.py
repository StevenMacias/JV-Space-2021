# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:36:39 2022

@author: Jordi Castillo
"""
from sense_hat import SenseHat

sense = SenseHat() 
sense.set_imu_config(True, False, False) 

def getMagnetometerValues():
    # Code to obtain values from the Magnetometer
    magnetometer_values = sense.get_compass_raw()
    # Code for filling magnetometer_values
    return magnetometer_values


def main():
   print("JV-Space")
   mag = getMagnetometerValues()
   print(mag)
   
if __name__ == "__main__":
    main()