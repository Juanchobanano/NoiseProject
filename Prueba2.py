# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:07:18 2019

@author: Juan Esteban Cepeda
"""

# Import libraries.
import pandas as pd
import numpy as np
import os
import random

import folium
from folium import plugins
from folium.plugins import HeatMap

# Load audio & GPS files.
pathFile =  "./coordenadas.csv"

df = pd.read_csv(pathFile, delimiter = ";", decimal = ",", float_precision='high')
df.columns = "registro lat lon".split()
df = df[["lat", "lon"]]
df.dropna(inplace = True)
df["noise"] = 50.6581684651



heat_data = [[row['lat'], row['lon'], row["noise"]] for index, row in df.iterrows()]

for d in heat_data:
    #print(d, end='\n')
    if len(d[:2]) != 2:
        print("error")
#heat_data = [(row['lat'], row['lon'], row["noise"]) for index, row in df.iterrows()] # , row["Weight"]] 

#print(heat_data)



map_hooray = folium.Map(location=[4.638594, -74.084442], zoom_start = 16) # , width = 800, height = 480)
folium.PolyLine(heat_data, maxval = 10, color="red", weight=2.5, opacity=1).add_to(map_hooray)
HeatMap(line).add_to(map_hooray)
map_hooray.save("./Mapas/Prueba2.html")