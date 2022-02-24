# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:36:39 2022

@author: Bernat Casas, Jordi Castillo, Nadia González, Steven Macías, Eric Pérez
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
    """
    Function used to obtain the magnetometer values
    """
    magnetometer_values = None
    logger.info('Getting magnetometer values')
    # Code to obtain values from the Magnetometer
    try:
        # Try-catch just in case of hardware fail
        magnetometer_values = sense.get_compass_raw()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})') 
        
    logger.info(f'Magnetometer values: {magnetometer_values}')
    return magnetometer_values

def get_iss_position():
    """
    Function used to obtain the ISS location
    """
    logger.info('Getting the ISS position')
    # Obtain the current time `t`
    t = load.timescale().now()
    # Compute where the ISS is at time `t`
    position = ISS.at(t)
    # Compute the coordinates of the Earth location directly beneath the ISS
    location = position.subpoint()
    logger.info(f'The location of the ISS: {location}')
    return location

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    logger.info(f'Conversion of the coordinates: {angle}')
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture_image(camera, image):
    """
    Use `camera` to capture an `image` file with lat/long EXIF data.
    """
    
    logger.info('Capturing image...')
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
        logger.info(f"Trying to capture image at {image}")
        camera.capture(image)
        logger.info("Image captured.")
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})') 
    
def create_csv(data_file):
    """
    Function used to create the header of the CSV file
    """
    with open(data_file, 'w') as f:
        logger.info('Creating header of CSV file')
        writer = csv.writer(f)
        header = ("iter", "datetime", "mag_x", "mag_y", "mag_z", "iss_pos_lat", "iss_pos_lon", "iss_pos_elv", "image_name", "is_sunlit")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """
    Function used to add a new row to the CSV File
    """
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        logger.info(f'Writing row of data: {data}')
        writer.writerow(data)
        
def get_sunlight(ephemeris,timescale):
    """
    Function used to know if the picture will be bright or in the darkness
    """
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
    logger.info("Executing experiment from JV-Space")
    
    camera_ready    = False
    ephemeris_ready = False 
    sensehat_ready  = False
    
    # Creating and configuring camera. 
    try:
        # Try-catch just in case of camera failure
        camera = PiCamera()
        camera.resolution = (2592, 1944)
        camera_ready = True 
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
         
    # Creating and configuring Sense Hat 
    try:
        # Try-catch just in case of sense hat failure
        sense = SenseHat() 
        sense.set_imu_config(True, False, False) 
        sensehat_ready = True
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
        
    # Obtaining ephemeris
    try:
        # Try-catch just in case of corrupted built-in file or no connection
        ephemeris=load("de421.bsp")
        timescale=load.timescale()
        ephemeris_ready = True
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    
    logger.warning("This is the result of the initialization progress")
    logger.info(f"Is camera ready? : {camera_ready}")
    logger.info(f"Ephemeris ready? : {ephemeris_ready}")
    logger.info(f"Is SenseHat ready? : {sensehat_ready}")
    
    logger.info("Obtaining path where the script is being executed...")
    base_folder = Path(__file__).parent.resolve()
    logger.info(f"The path is: {base_folder}")
    
    # Path where the CSV,the log file and the images are going to be saved
    data_file    = base_folder/'data.csv'
    log_file     = base_folder/"events.log"
    image_folder = base_folder/"images"
    
    # Creating log file 
    logfile(log_file)
    
    logger.info(f"Creating image folder at {image_folder}")
    os.makedirs(image_folder, exist_ok=True)
    # Create header of the CSV file
    create_csv(data_file)
    
    # Defining time variables
    start_time = datetime.now()
    logger.info(f'Experiment started at {start_time}')
    now_time = datetime.now()
    
    iteration = 0
    sleep_time = 15
    experiment_minutes = 179
    # We are expecting to take 716 pictures in 179 minutes. 
    # By using the maximum size of the example images with resolution (2592x1944) 
    # in the provided Data folder (3.5 MB), we expect to use 2506 MB
    while (now_time < start_time + timedelta(minutes=experiment_minutes)):
        logger.info(f"Iteration {iteration}")
        
        # Image capturing code 
        image_name = f"image_{iteration:04d}.jpg"
        image_path = image_folder/image_name
        if camera_ready : capture_image(camera, str(image_path))
        
        # Obtaining magnetometer values
        if sensehat_ready : 
            mag = get_magnetometer_values(sense)
        else: 
            # fake structure to avoid code crashing in other points
            mag = {"x":None, "y":None, "z":None}
            
        # Obtaining ISS Position
        iss_pos = get_iss_position()
        
        # Obtaining sunlight values
        if ephemeris_ready : 
            sunlit = get_sunlight(ephemeris, timescale)
        else:
            sunlit = None
            
        # Generating new row for the CSV file
        row = (
            iteration,
            datetime.now(),
            mag["x"], mag["y"], mag["z"],
            iss_pos.latitude.degrees,
            iss_pos.longitude.degrees,
            iss_pos.elevation.km,
            image_name,
            sunlit
            )
        
        logger.info('Updating the CSV file')
        add_csv_data(data_file, row)
        logger.info("Sleeping during 15 seconds...")
        sleep(sleep_time)
        now_time = datetime.now()
        logger.info(f"Current time: {now_time}")
        iteration = iteration + 1
    
    # Goodbye code
    if camera_ready: camera.close()
    logger.info(f"Experiment finished at: {now_time}.")
    logger.info(f"Executed {iteration} iterations.")
    logger.info("Thank you so much! We are done :)")
    
if __name__ == "__main__":
    main()
