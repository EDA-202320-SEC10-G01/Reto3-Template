﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
import numpy as np
from datetime import datetime as datetime
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    control = {"earthquakes_list": lt.newList("ARRAY_LIST"),
               "earthquakes_tree_date": None,
               "earthquakes_tree_mag": None,
               "earthquakes_tree_depth": None}
    
    return control


def add_data(control, data):
    """
    Adiciona un dato a las estructuras de datos del modelo
    """
    lt.addLast(control["earthquakes_list"], data)
    

def create_tree_time(control):
    
    def comparacion_llaves(earthquake1, earthquake2):
        
        codigo1, time1 = earthquake1.split("^")
        codigo2, time2 = earthquake2.split("^")
        
        if comparar_tiempos(time1, time2) == 1:
            return 1
        elif comparar_tiempos(time1, time2) == 0:
            if codigo1 > codigo2:
                return 1
            elif codigo1 == codigo2:
                return 0
            else:
                return -1
        else:
            return -1
    
    tree = om.newMap(omaptype="RBT", cmpfunction=comparacion_llaves)
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        om.put(tree, f"{earthquake["code"]}^{earthquake["time"]}" , earthquake)
        
    return tree


def create_tree_mag(control):
    
    def comparacion_llaves(earthquake1, earthquake2):
        
        codigo1, mag1 = earthquake1.split("^")
        codigo2, mag2 = earthquake2.split("^")
        
        if float(mag1) > float(mag2):
            return 1
        elif float(mag1) == float(mag2):
            if codigo1 > codigo2:
                return 1
            elif codigo1 == codigo2:
                return 0
            else:
                return -1
        else:
            return -1
    
    tree = om.newMap(omaptype="RBT", cmpfunction=comparacion_llaves)
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        om.put(tree, f"{earthquake["code"]}^{earthquake["mag"]}" , earthquake)
        
    return tree
    

#Requerimientos

def req_1(control, fecha_inicial, fecha_final):
    
    lista_por_año = lt.newList()
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        if (comparar_tiempos(earthquake["time"], fecha_inicial) == 1 and comparar_tiempos(earthquake["time"], fecha_final) == -1) or comparar_tiempos(earthquake["time"], fecha_inicial) == 0 or comparar_tiempos(earthquake["time"], fecha_final) == 0:
            lt.addLast(lista_por_año, earthquake)
            
    merg.sort(lista_por_año, lambda x, y: comparar_tiempos(x["time"], y["time"]) == 1)
    
    return lista_por_año, lt.size(lista_por_año)


def req_2(control, magnitud_inicial, magnitud_final):
    
    lista_por_magnitud = lt.newList()
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        if float(earthquake["mag"]) >= float(magnitud_inicial) and float(earthquake["mag"]) <= float(magnitud_final):
            lt.addLast(lista_por_magnitud, earthquake)
            
    merg.sort(lista_por_magnitud, lambda x, y: float(x["mag"]) > float(y["mag"]))
    
    return lista_por_magnitud
def req_3(control, mag_min, depth_max):
    # Crear una lista para almacenar los eventos que cumplen con los criterios
    eventos_filtrados = lt.newList()

    # Filtrar los eventos según la magnitud y profundidad
    for earthquake in lt.iterator(control["earthquakes_list"]):
        mag = earthquake["mag"]
        depth = earthquake["depth"]

        if mag >= mag_min and depth <= depth_max:
            lt.addLast(eventos_filtrados, earthquake)

    
    return eventos_filtrados

def req_4(control, sig_min, gap_max):
    # Crear una lista para almacenar los eventos que cumplen con los criterios
    eventos_filtrados = lt.newList()

    # Filtrar los eventos según la significancia y el gap
    for earthquake in lt.iterator(control["earthquakes_list"]):
        sig = earthquake["sig"]
        gap = earthquake["gap"]

        if sig >= sig_min and gap <= gap_max:
            lt.addLast(eventos_filtrados, earthquake)

    
    eventos_filtrados = sorted(lt.toArray(eventos_filtrados), key=lambda x: x["date"], reverse=True)

    
    eventos_recientes = eventos_filtrados[:10]

    return eventos_recientes

def req_5(control, depth_min, nst_min):
    # Crear una lista para almacenar los eventos que cumplen con los criterios
    tree = om.newMap(omaptype="RBT", cmpfunction=comparacion_llaves)
    for earthquake in lt.iterator(control["earthquakes_list"]):
    depth_min = float(depth_min)
    nst_min = float(nst_min)
    key = f"{depth}-{nst}"
    eventos = om.put(tree, key, earthquake)
    return eventos


def req_6(control, año, latitud, longitud, radio, n_eventos):
    
    def haversine_function(lat1, lon1, lat2, lon2):
        
        earth_radius = 6371
        
        lat1 = np.radians(float(lat1))
        lat2 = np.radians(float(lat2))
        lon1 = np.radians(float(lon1))
        lon2 = np.radians(float(lon2))
        
        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1
        
        a = (np.sin(lat_diff/2))**2
        b = np.cos(lat1)
        c = np.cos(lat2)
        d = (np.sin(lon_diff/2))**2       
        e = a + b*c*d
        
        
        return 2 * earth_radius * np.arcsin(np.sqrt(e))
            
              
    lista_por_año_distancia = lt.newList()
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        if earthquake["time"].split("T")[0].split("-")[0] == año and haversine_function(earthquake["lat"], earthquake["long"], latitud, longitud) <= float(radio):
            lt.addLast(lista_por_año_distancia, earthquake)
            
            
    mayor_magnitud = max(lt.iterator(lista_por_año_distancia), key=lambda x: x["mag"])
    
    lista_mas_cercanos = lt.newList()
    
    for earthquake in lt.iterator(lista_por_año_distancia):
        if earthquake != mayor_magnitud:
            
            time_diff = diferencias_de_fechas(mayor_magnitud["time"], earthquake["time"])
            earthquake["time_diff"] = time_diff
            print(time_diff)
            
            lt.addLast(lista_mas_cercanos, earthquake)
            
    merg.sort(lista_mas_cercanos, lambda x, y: x["time_diff"] > y["time_diff"])
    
    return lista_mas_cercanos
                
def comparar_tiempos(date_time1, date_time2):  
    
    date_time1 = datetime.strptime(date_time1, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_time2 = datetime.strptime(date_time2, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    if date_time1 > date_time2:
        return 1
    elif date_time1 == date_time2:
        return 0
    else:
        return -1
            
def diferencias_de_fechas(date_time1, date_time2):
 
    if comparar_tiempos(date_time1, date_time2) == 1:
        
        date_time1 = datetime.strptime(date_time1, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_time2 = datetime.strptime(date_time2, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        return date_time1 - date_time2
    
    else:
        
        date_time1 = datetime.strptime(date_time1, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_time2 = datetime.strptime(date_time2, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        return date_time2 - date_time1