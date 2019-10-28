# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:44:25 2019

@author: Juan Esteban Cepeda
"""


import folium
import folium.plugins as plugins
import numpy as np

np.random.seed(3141592)
initial_data = (
    np.random.normal(size=(100, 2)) * np.array([[1, 1]]) +
    np.array([[48, 5]])
)

move_data = np.random.normal(size=(100, 2)) * 0.01

data = [(initial_data + move_data * i).tolist() for i in range(100)]

weight = 1  # default value
for time_entry in data:
    for row in time_entry:
        row.append(weight)
        
m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)

hm = plugins.HeatMapWithTime(data)

hm.add_to(m)

m.save("holamundo.html")