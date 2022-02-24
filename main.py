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

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()
    
    #Convert the latitude and longitude to EXIF-appropiate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)
    
    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
    
    # Capture the image
    try:
        logger.info(f"Trying to save image at {image}")
        camera.capture(image)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})') 
    
def create_csv(data_file):
    with open(data_file, 'w') as f:
        logger.info('Creating header of CSV file')
        writer = csv.writer(f)
        header = ("iter", "datetime", "mag_x", "mag_y", "mag_z", "iss.pos_lat", "iss.pos_lon", "iss.pos_elv", "image_name", "sunlit")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        logger.info('Writing row of data')
        writer.writerow(data)
        
def get_sunlight(ephemeris,timescale):
    t = timescale.now()
    result = None
    if ISS.at(t).is_sunlit(ephemeris):
        logger.info('In sunlight')
        result = True
    else:
        logger.info('In darkness')
        result = False
    return result

def main():
   logger.info("Executing JV-Space's program")
   camera = PiCamera()
   camera.resolution = (1680, 1050)
   sense = SenseHat() 
   sense.set_imu_config(True, False, False) 
   base_folder = Path(__file__).parent.resolve()
   data_file = base_folder/'data.csv'
   logfile(base_folder/"events.log")
   iteration = 0
   image_folder = base_folder/"images"
   ephemeris=load("de421.bsp")
   timescale=load.timescale()
   os.makedirs(image_folder, exist_ok=True)
   create_csv(data_file)
   # Create a `datetime` variable to store the start time
   start_time = datetime.now()
   logger.info(f'Experiment started at {start_time}')
   # Create a `datetime` variable to store the current time
   # (these will be almost the same at the start)
   now_time = datetime.now()
   # Run a loop for 180 minutes
   while (now_time < start_time + timedelta(minutes=178)):
       image_name = f"image_{iteration:03d}.jpg"
       image_path = image_folder/image_name
       capture(camera, str(image_path))
       mag = get_magnetometer_values(sense)
       iss_pos = get_iss_position()
       row = (iteration, datetime.now(), mag["x"], mag["y"], mag["z"], iss_pos.latitude.degrees, iss_pos.longitude.degrees, iss_pos.elevation.km, image_name, get_sunlight(ephemeris, timescale))
       add_csv_data(data_file, row)
       sleep(15)
       now_time = datetime.now()
       iteration = iteration + 1
   
if __name__ == "__main__":
    main()
