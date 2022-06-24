import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv_location = "/home/pi/Desktop/Processed_Pictures_2/processed_data_2.csv"
df = pd.read_csv(csv_location) 

plt.scatter(df.Mag_val, df.NDVI_val)
plt.ylim(-0.75, 0.75)
plt.title("NDVI - Magnetomer")
plt.xlabel("Magnetometer absolute value")
plt.ylabel("Average NDVI of the images ")
plt.show()

print(df[df["NDVI_val"]>0.4]["image_name"])