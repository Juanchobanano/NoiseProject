import pandas as pd 
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap
import datetime
import random

def generateTimes(df, dt, end, step = 15):
    step = datetime.timedelta(seconds = step)
    result = []
    contador = 0
    
    while dt < end and contador < len(df):
        result.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
        dt += step
        contador += 1
    df2 = pd.DataFrame(data = result, columns = ["Date"])
    return df2

def modifyCoordinates(df, hour):
    
    data = df.copy()
    lat = data["lat"].values
    lon = data["lon"].values
    noise = data["noise"].values
    
    #print(hour == 18)
    
    for i in range(0, len(lat)):
        r1 = random.uniform(0.000001, 0.000099)
        r2 = random.uniform(0.000001, 0.000099)
        signo = random.randint(1, 2)
        if(signo == 1): signo = 1
        else: signo = -1
            
        lat[i] = lat[i] + signo * r1
        lon[i] = lon[i] + signo * r2
        
        r3 = 0
        if(hour == 7): r3 = random.uniform(10, 20)
        elif(hour == 11): r3 = random.uniform(15, 25)
        elif(hour == 14): r3 = random.uniform(20, 30)
        elif(hour == 16): r3 = random.uniform(5, 15)
        elif(hour == 18): r3 = -random.uniform(20, 30)
        
        #if(noise[i] < 60):
        #    noise[i] = (noise[i] + r3)
        #noise[i] /= 10
        
        noise[i] = noise[i] + r3
        noise[i] = noise[i] / 100
        
    df2 = pd.DataFrame(data = lat, columns = ["lat"])
    df3 = pd.DataFrame(data = lon, columns = ["lon"])
    df4 = pd.DataFrame(data = noise, columns = ["noise"])
    
    
    df_temp = df2.join(df3)
    df_temp = df_temp.join(df4)

    return df_temp
    

pathFile = "./coordenadas.csv"
df = pd.read_csv(pathFile, delimiter = ";", decimal = ",", float_precision = "high")
df.columns = "registro lat lon noise".split()
df = df[["lat", "lon", "noise"]]
df.dropna(inplace = True)

days = [7, 8, 9, 10, 11]
hours = [7, 9, 11, 14, 16, 18]
df_array = list()
df_copy = pd.DataFrame(data = None)


for d in days:
    
    df_copy.iloc[0:0]
    df_copy = df.copy()
    
    for h in hours: 
        
        dt = datetime.datetime(2019, 11, d, h, 0, 0)
        end = datetime.datetime(2019, 11, d, h + 2, 0, 0)
        dates = generateTimes(df, dt, end, 15)
        df_final = modifyCoordinates(df_copy, h)
        df_final = df_final.join(dates)
        df_final.set_index("Date", inplace = True)
        df_array.append(df_final)
        df_final.iloc[0:0]
        
        
for i in range(0, len(df_array)):
    
    #print(i)
    
    # Create map instance. 
    map_hooray = folium.Map(location=[4.6378758, -74.0839653], zoom_start = 16)
    
    # Get Data. 
    data = df_array[i].copy()
    print(data)

    # Generate path & add markers.
    path_data = [[row['lat'],row['lon']] for index, row in data.iterrows()] 
    #folium.PolyLine(path_data, maxval = 10, color="red", weight=2.5, opacity=1).add_to(map_hooray)
    folium.Marker(path_data[0], popup='<i>Inicio Trayecto. Hora:' +  data.index[0] + '</i>', icon=folium.Icon(icon='cloud')).add_to(map_hooray)
    folium.Marker(path_data[-1], popup='<i>Fin Trayecto. Hora: ' +  data.index[-1] + '</i>', icon=folium.Icon(color='red', icon='info-sign')).add_to(map_hooray)
    
    # Markers Path.
    #for d in range(0, len(path_data)):
    #    folium.Marker(path_data[d], popup = str(path_data[d]) + " " + str(d)) .add_to(map_hooray)
    
    # Generate heat map.
    heat_data = [[row['lat'],row['lon'], row["noise"]] for index, row in data.iterrows()] # , row["Weight"]] 
    HeatMap(heat_data, name = "Mapa de Ruido UNAL", max_val = 1, radius = 25, min_opacity = 0.42).add_to(map_hooray)
     
    # Display the map
    map_hooray.save("./AutoGenerados/" + str(data.index[0][0:10]) + "-" + str(hours[i % len(hours)]) + ".html")

