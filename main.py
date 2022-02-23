# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:36:39 2022

@author: Bernat Casas, Jordi Castillo, Nadia González, Steven Macías
"""
from datetime import datetime, timedelta
from logzero import logger, logfile
from sense_hat import SenseHat
from skyfield.api import load
from picamera import PiCamera
from pathlib import Path
from time import sleep
from orbit import ISS
import csv
import os


camera = PiCamera()
camera.resolution = (1680, 1050)
os.mkdir("./images")
def get_magnetometer_values(sense):
    # Code to obtain values from the Magnetometer
    magnetometer_values = sense.get_compass_raw()
    # Code for filling magnetometer_values
    return magnetometer_values

def get_iss_position():
    # Obtain the current time `t`
    t = load.timescale().now()
    # Compute where the ISS is at time `t`
    position = ISS.at(t)
    # Compute the coordinates of the Earth location directly beneath the ISS
    location = position.subpoint()
    return location
    
    
def create_csv(data_file):
    with open(data_file, 'w') as f:
        logger.info('Creating header of CSV file')
        writer = csv.writer(f)
        header = ("iter", "datetime", "mag_x", "mag_y", "mag_z", "iss.pos_lat", "iss.pos_lon", "iss.pos_elv")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        logger.info('Writing row of data')
        writer.writerow(data)

def main():
   logger.info("Executing JV-Space's program")
   sense = SenseHat() 
   sense.set_imu_config(True, False, False) 
   base_folder = Path(__file__).parent.resolve()
   data_file = base_folder/'data.csv'
   logfile(base_folder/"events.log")
   iteration = 0

   create_csv(data_file)
   # Create a `datetime` variable to store the start time
   start_time = datetime.now()
   logger.info('Experiment started at {start_time}')
   # Create a `datetime` variable to store the current time
   # (these will be almost the same at the start)
   now_time = datetime.now()
   # Run a loop for 180 minutes
   while (now_time < start_time + timedelta(minutes=178)):
       mag = get_magnetometer_values(sense)
       iss_pos = get_iss_position()
       row = (iteration, datetime.now(), mag["x"], mag["y"], mag["z"], iss_pos.latitude.degrees, iss_pos.longitude.degrees, iss_pos.elevation.km)
       add_csv_data(data_file, row)
       camera.capture(f'./images/image_{iteration:03d}.jpg')
       sleep(15)
       now_time = datetime.now()
       iteration = iteration + 1
   
if __name__ == "__main__":
    main()
