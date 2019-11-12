# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:00:59 2019

@author: Juan Esteban Cepeda
"""

# Import libraries.
import pandas as pd
import numpy as np
import os

import folium
from folium import plugins
from folium.plugins import HeatMap


# Load audio & GPS files.
pathFile =  "./Resultados/"
csv_files = list()

# Get CSV files.
with os.scandir(pathFile) as entries:
    for entry in entries:
        csv_files.append(entry.name)
        
# Get audio-gps author.
def author(id):
    if id == 1: return "Daniel"
    elif id == 2: return "Juan Esteban"
    elif id == 3: return "Carlos"
    elif id == 4: return "Tania"
        

def generateMap(df):

    # Initialize map.
    map_hooray = folium.Map(location=[4.6365, -74.0815], tiles='stamentoner', zoom_start = 16 , width = 800, height = 480)

    # Get Data.
    latitude = list()
    longitude = list()
    weight = list()

    for i in range(0, len(df)):
        latitude.append(float(str(df.iloc[i]["lat"]).replace(",",".")))
        longitude.append(float(str(df.iloc[i]["lon"]).replace(",",".")))
        weight.append(float(str(df.iloc[i]["Noise"]).replace(",",".")))

    data = pd.DataFrame(data={"Latitude": latitude, "Longitude": longitude, "Weight": weight})
    #print(data)

    # List comprehension to make out list of lists
    heat_data = [np.array([row['Latitude'],row['Longitude'], row["Weight"]]) for index, row in data.iterrows()]  #, row["Weight"]

    # Plot it on the map
    HeatMap(heat_data).add_to(map_hooray)

    #Add markers
    folium.Marker(heat_data[0], popup='<i>Inicio Trayecto. Hora:' +  df.iloc[0]["time"] + '</i>',).add_to(map_hooray)
    folium.Marker(heat_data[-1], popup='<i>Fin Trayecto. Hora: ' +  df.iloc[-1]["time"] + '</i>',).add_to(map_hooray)

    folium.PolyLine(heat_data, maxval = 1.1, color="red", weight=2.5, opacity=1).add_to(map_hooray)

    # Display the map
    return map_hooray



for i in range(0, len(csv_files)):
    
    df = pd.read_csv("./Resultados/" + csv_files[i])
    df = df.drop("Unnamed: 0", axis = 1)
    
    print(author(int(csv_files[i][0])))
    print(csv_files[i])
      
    generateMap(df).save("./Mapas/" + csv_files[i].replace("csv", "") + ".html")


"""
data = (
    np.random.normal(size=(100, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[48, 5, 1]])
).tolist()


from folium.plugins import HeatMap

m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)

HeatMap(data).add_to(m)

m.save(os.path.join('Mapas', 'Heatmap.html'))
"""