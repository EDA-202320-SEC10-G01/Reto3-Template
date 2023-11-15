"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
sys.setrecursionlimit(10000)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    tamaño = input("""Ingrese el numero asociado al tamaño de la muestra: \n
    1. Small \n
    2. 5% \n
    3. 10 % \n
    4. 20 % \n
    5. 30 % \n
    6. 50 % \n
    7. 80 % \n
    8. Large \n""")
    
    tiempo_carga, memoria = controller.load_data_file(control, tamaño)

    print("=============== Carga de Datos ==================")
    print(f"\nTiempo de carga: {tiempo_carga} ms")
    print(f"\nMemoria utilizada: {memoria} MB")
    
    
def print_table(table, columns):
    
    if lt.size(table) == 0:
        print("No hay datos para mostrar")
        
    elif lt.size(table) > 10:
        first_five = lt.subList(table, 1, 5)
        last_five = lt.subList(table, lt.size(table)-4, 5)
        combined_list = lt.newList("ARRAY_LIST")
        
        for i in lt.iterator(first_five):
            lt.addLast(combined_list, i)
            
        for i in lt.iterator(last_five):
            lt.addLast(combined_list, i)
            

        combined_list = columns_to_show(combined_list, columns)
            
        print(f"\nDe {lt.size(table)} elementos, se muestran los primeros y últimos 5\n")
        print(tabulate(lt.iterator(combined_list), headers = "keys", tablefmt = "fancy_grid"))
    
    else:
        
        new_table = columns_to_show(table, columns)
        print(f"\n Se encontraron {lt.size(table)} elementos mostrados a continuacion\n")
        print(tabulate(lt.iterator(table), tablefmt = "fancy_grid"))
        

def columns_to_show(list_dicts, columns):
    
    new_table = lt.newList("ARRAY_LIST")
    
    for i in lt.iterator(list_dicts):
        new_dict = {}
        for j in columns:
            new_dict[j] = i[j]
        lt.addLast(new_table, new_dict)
        
    return new_table


def print_data(control):
    
    columns_to_show = ["time", "lat", "long", "depth", "mag", "sig", "nst", "gap", "title", "felt", "cdi", "mmi", "tsunami"]
    
    print_table(control["earthquakes_list"], columns_to_show)
    

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # Se obtiene la información solicitada al modelo
    fecha_inicial = input("Ingrese la fecha inicial en formato AAAA-MM-DDTHH:MM:SS\n")
    fecha_final = input("Ingrese la fecha final en formato AAAA-MM-DDTHH:MM:SS\n")

    #Se establecen los encabezados de la tabla
    columns_to_show = ["time", "lat", "long", "depth", "mag", "sig", "nst", "gap", "title", "felt", "cdi", "mmi", "tsunami"]
    # Se llama la funcion del controlador para obtener los datos
    data = controller.req_1(control, fecha_inicial, fecha_final)
    time,mag,lat,long,depth, sig,gap,nst,title,cdi,mmi,magType,type,code  = data
    # Se imprime la tabla
    print_table(code, data)


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    año = input("Ingrese el año a buscar\n")
    latitud = input("Ingrese la latitud a buscar\n")
    longitud = input("Ingrese la longitud a buscar\n")
    radio = input("Ingrese el radio a buscar\n")
    n_eventos = input("Ingrese el numero de eventos a buscar\n")
    columnas = ["time", "mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    
    
    data = controller.req_6(control, año, latitud, longitud, radio, n_eventos)
    
    print_table(data, columnas) 

# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            print_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
