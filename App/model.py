"""
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
    control = {"earthquakes_list": lt.newList("ARRAY_LIST")}
    
    return control


def add_data(control, data):
    """
    Adiciona un dato a las estructuras de datos del modelo
    """
    lt.addLast(control["earthquakes_list"], data)
    
    
def req_1(control, date_time1, date_time2):
    
    comparar = comparar_fechas_hora(data1, data2)
    tree_dates = om.newMap(omaptype="RBT", comparar)
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        
        date_time = earthquake["time"][0:-1]
        mp.put(tree_dates, date_time, earthquake)
    
    lista_fechas = om.keys(tree_dates, date_time1, date_time2)
    
    return lista_fechas


def req_2(control,inf_mag,sup_mag):
    tree_mag = om.newMap(omaptype="RBT")
    for earthquake in lt.iterator(control["earthquakes_list"]):
        mag = earthquake["mag"]
        if mag >= inf_mag and mag <= sup_mag:
            mp.put(tree_mag, mag, earthquake)
    list_mag = om.keys(tree_mag, inf_mag, sup_mag)
    return list_mag
    
def req_6(control, año, latitud, longitud, radio, n_eventos):
    
    def haversine_function(lat1, lon1, lat2, lon2):
        
        earth_radius = 6371
        
        lat1 = np.radians(lat1)
        lat2 = np.radians(lat2)
        lon1 = np.radians(lon1)
        lon2 = np.radians(lon2)
        
        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1
        
        a = (np.sin(lat_diff/2))**2
        b = np.cos(lat1)
        c = np.cos(lat2)
        d = (np.sin(lon_diff/2))**2       
        e = a + b*c*d
        
        return 2 * earth_radius * np.arcsin(np.sqrt(e))
            
    def sort_req_6(data1, data2):
        
        if comparar_fechas_hora(data1["time_diff"], data2["time_diff"]) == 1:
            return True
        else:
            return False
              
    lista_por_año = lt.newList()
    
    for earthquake in lt.iterator(control["earthquakes_list"]):
        if earthquake["time"].split("T")[0].split("-")[0] == año:
            lt.addLast(lista_por_año, earthquake)
            
            
    mayor_magnitud = max(lt.iterator(lista_por_año), key=lambda x: x["mag"])
    
    eventos_proximos = lt.newList()
    
    for earthquake in lt.iterator(lista_por_año):
        
        if earthquake != mayor_magnitud:
        
            if haversine_function(earthquake["lat"], earthquake["long"], mayor_magnitud["lat"], mayor_magnitud["long"]) <= radio:
                earthquake["time_diff"] = diferencias_de_fechas(earthquake["time"], mayor_magnitud["time"])
                lt.addLast(eventos_proximos, earthquake)
                
                
    mg.sort(eventos_proximos, sort_req_6)
    
    return eventos_proximos
                
                
    
            
            

#Funciones para comparar fechas y horas   
def comparar_fechas_hora(date_time1, date_time2):
    
    date1, time1 = date_time1.split("T")
    date2, time2 = date_time2.split("T")
    year1, month1, day1 = date1.split("-")
    year2, month2, day2 = date2.split("-")
    hour1, minute1, second1 = time1.split(":")[:-1], round(time1.split(":")[2],3)
    hour2, minute2, second2 = time2.split(":")[:-1], round(time2.split(":")[2],3)
    
    if int(year1) > int(year2):
        return 1
    elif int(year1) == int(year2):
        if int(month1) > int(month2):
            return 1
        elif int(month1) == int(month2):
            if int(day1) > int(day2):
                return 1
            elif int(day1) == int(day2):
                if int(hour1) > int(hour2):
                    return 1
                elif int(hour1) == int(hour2):
                    if int(minute1) > int(minute2):
                        return 1
                    elif int(minute1) == int(minute2):
                        if int(second1) > int(second2):
                            return 1
                        elif int(second1) == int(second2):
                            return 0
                        else:
                            return -1
                    else:
                        return -1
                else:
                    return -1
            else:
                return -1
            
def diferencias_de_fechas(date_time1, date_time2):
    
    date1, time1 = date_time1.split("T")
    date2, time2 = date_time2.split("T")
    year1, month1, day1 = date1.split("-")
    year2, month2, day2 = date2.split("-")
    hour1, minute1, second1 = time1.split(":")[:-1], round(time1.split(":")[2],3)
    hour2, minute2, second2 = time2.split(":")[:-1], round(time2.split(":")[2],3)
    
    if comparar_fechas_hora(date_time1, date_time2) == 1:
        
        diff_year = int(year1) - int(year2)
        diff_month = int(month1) - int(month2)
        diff_day = int(day1) - int(day2)
        diff_hour = int(hour1) - int(hour2)
        diff_minute = int(minute1) - int(minute2)
        diff_second = float(second1) - float(second2)
        
        return f"{diff_year}-{diff_month}-{diff_day}T{diff_hour}:{diff_minute}:{diff_second}"
    
    else:
        
        diff_year = int(year2) - int(year1)
        diff_month = int(month2) - int(month1)
        diff_day = int(day2) - int(day1)
        diff_hour = int(hour2) - int(hour1)
        diff_minute = int(minute2) - int(minute1)
        diff_second = float(second2) - float(second1)
        
        return f"{diff_year}-{diff_month}-{diff_day}T{diff_hour}:{diff_minute}:{diff_second}"