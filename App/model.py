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
    

def comparar_fechas(fecha_1, fecha_2):
    
    #Retorna 1 si la fecha 1 es mayor que la fecha 2
    #Retorna 0 si las fechas son iguales
    #Retorna -1 si la fecha 1 es menor que la fecha 2
    
    fecha_1 = fecha_1.split("-")
    fecha_2 = fecha_2.split("-")
    
    
    if int(fecha_1[0]) > int(fecha_2[0]):
        return 1
    elif int(fecha_1[0]) == int(fecha_2[0]):
        if int(fecha_1[1]) > int(fecha_2[1]):
            return 1
        elif int(fecha_1[1]) == int(fecha_2[1]):
            if int(fecha_1[2]) > int(fecha_2[2]):
                return 1
            elif int(fecha_1[2]) == int(fecha_2[2]):
                return 0
            else:
                return -1
        else:
            return -1
    else:
        return -1

def intervalo(fecha_inicial, fecha_final, fecha):
    
    #Retorna True si la fecha esta dentro del intervalo y False si no lo está
    
    if comparar_fechas(fecha, fecha_inicial) == 1 and comparar_fechas(fecha, fecha_final) == -1:
        return True
    elif comparar_fechas(fecha, fecha_inicial) == 0 or comparar_fechas(fecha, fecha_final) == 0:
        return True
    else:
        return False
    
def req_1(control, fecha_inicial, fecha_final):
    
    #Retorna una lista con los sismos que ocurrieron en el intervalo de tiempo dado
    
    lista_sismos = lt.newList("ARRAY_LIST")
    
    for i in lt.iterator(control["earthquakes_list"]):
        if intervalo(fecha_inicial, fecha_final, i["time"]):
            lt.addLast(lista_sismos, i)
    
    return lista_sismos    