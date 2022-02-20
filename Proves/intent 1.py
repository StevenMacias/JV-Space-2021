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
    
    
    
    
start_time = time.time()
seconds = 10

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > seconds:
        print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
        break


import csv

header = ['magnetometer values']
data = [
    [def main]
]
#https://www.pythontutorial.net/python-basics/python-write-csv-file/