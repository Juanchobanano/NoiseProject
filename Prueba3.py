# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:45:19 2019

@author: Juan Esteban Cepeda
"""


import os
import folium

print(folium.__version__)


import numpy as np

data = (
    np.random.normal(size=(100, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[48, 5, 1]])
).tolist()

for d in data:
    #print(d, end='\n')
    print(d[:2])

from folium.plugins import HeatMap

m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)

HeatMap(data).add_to(m)

m.save("./Mapas/Heatmap.html")