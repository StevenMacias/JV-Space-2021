# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 23:59:04 2022

@author: joanf
"""

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
    
    
    
    
#In addition, any files that your program creates should have sensible, 
#informative names. Only use letters, numbers, dots (.), hyphens (-), 
#or underscores (_) in your file names. 
#No other characters are allowed. Do not use spaces in file names, 
#because they can cause problems when files are transferred between computers.

import csv
from sense_hat import SenseHat
from datetime import datetime
from pathlib import Path
from time import sleep

def create_csv(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Magnetometer Values")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

sense = SenseHat()

base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'

create_csv(data_file)
for i in range(10):
    row = (datetime.now(), sense.magnetism)
    add_csv_data(data_file, row)
    sleep(10)
    
    
    from orbit import ISS
from skyfield.api import load

# Obtain the current time `t`
t = load.timescale().now()
# Compute where the ISS is at time `t`
position = ISS.at(t)
# Compute the coordinates of the Earth location directly beneath the ISS
location = position.subpoint()
print(location)