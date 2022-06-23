# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 13:39:41 2022

@author: Jordi Castillo
"""

import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

plt.figure(figsize=(6,48))
plt.set_ylim(-1,1)

correlation_filepath = "../input/processed-data/processed_data.csv"
correlation_data = pd.read_csv(correlation_filepath)
sns.regplot(x=correlation_data['mag_val'], y=correlation_data['NDVI_val'])

