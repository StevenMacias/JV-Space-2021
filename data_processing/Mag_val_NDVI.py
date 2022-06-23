# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 18:42:41 2022

@author: Jordi Castillo
"""

import cv2
import numpy as np
import pandas as pd
from fastiecm import fastiecm

def display (image, image_name):
    image = np.array(image, dtype = float)/float(255) #convert to an array
    shape = image.shape
    height = int(shape[0]/2)
    width = int(shape[1]/2)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name) # create window
    cv2.imshow(image_name, image) # display image
    cv2.waitKey(0) #wait for key press
    cv2.destroyAllWindows()


def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

def add_csv_data(data_file, data):
    with open(data_file, 'NDVI_val') as f:
        writer = csv.writer(f)
        writer.writerow(ndvi)
    
# Config
dir_orig_pictures = '/home/pi/jv_space/images/'
dir_processed_pictures = "/home/pi/Desktop/Processed_Pictures/"
cropping = True
#lectura CSV
df = pd.read_csv("/home/pi/jv_space/
data.csv", index_col = "iter")
#insertar columna para valores NDVI
df.insert(len(df.columns), 'NDVI_val', None)
print(df)
#insertar columnas para valores del magnetometro
df.insert(len(df.columns), 'Mag_val', None)

for index, row in df.iterrows():
    print(index)
    original = cv2.imread(dir_orig_pictures+row.image_name) #load image
    if cropping:
        y=500
        x=500
        h=1100
        w=1500
        original = original[y:y+h, x:x+w]
        #cv2.imshow("cropped", original)
        #cv2.waitKey(0)
    contrasted = contrast_stretch(original)
    #display(contrasted, 'Contrasted original')
    cv2.imwrite(dir_processed_pictures+'contrasted_'+row.image_name, contrasted)
    ndvi = calc_ndvi(contrasted)
    # Save average NDVI value in the dataframe
    df['NDVI_val'][index]= ndvi.mean()
    
    ndvi_contrasted = contrast_stretch(ndvi)
    #display(ndvi_contrasted, 'NDVI Contrasted')
    #cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)
    #cv2.imwrite(dir_processed_pictures+'ndvi_'+row.image_name, ndvi)
    cv2.imwrite(dir_processed_pictures+'ndvi_contrasted_'+row.image_name, ndvi_contrasted)
    color_mapped_prep_ndvi_con = ndvi_contrasted.astype(np.uint8)
    color_mapped_image_ndvi_con = cv2.applyColorMap(color_mapped_prep_ndvi_con, fastiecm)
    #color_mapped_prep_ndvi = ndvi.astype(np.uint8)
    #color_mapped_image_ndvi = cv2.applyColorMap(color_mapped_prep_ndvi, fastiecm)
    #display(color_mapped_image, 'Color mapped')
    #print(color_mapped_image.mean())
    #cv2.imwrite('color_mapped_image.png', color_mapped_image)
    cv2.imwrite(dir_processed_pictures+'color_mapped_con_ndvi_'+row.image_name, color_mapped_image_ndvi_con)
    #cv2.imwrite(dir_processed_pictures+'color_mapped__ndvi'+row.image_name, color_mapped_image_ndvi)
    Mag_vector = sqrt( (mag_x**2) + (mag_y**2) + (mag_z**2))
    df['Mag_val'][index]
 
df.to_csv(dir_processed_pictures+'processed_data.csv')