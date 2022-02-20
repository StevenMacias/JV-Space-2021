# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 21:53:23 2022

@author: joanf
"""

#from orbit import ISS
#from skyfield.api import load
#from sense_hat import SenseHat
from datetime import datetime
from pathlib import Path
from time import sleep
import csv

def create_csv(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("datetime", "mag_x", "mag_y", "mag_z", "iss_pos")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def main():
   print("JV-Space")
   mag = {"x": 1.0,"y": 1.0,"z": 1.0}
   print(mag)
   base_folder = Path(__file__).parent.resolve()
   data_file = base_folder/'data.csv'

   create_csv(data_file)
   for i in range(10):
       row = (datetime.now(), mag["x"], mag["y"], mag["z"], "10,20")
       add_csv_data(data_file, row)
       sleep(10)
       
if __name__ == "__main__":
    main()
      