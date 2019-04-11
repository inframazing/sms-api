# -*- coding: utf-8 -*-

# +==========================================================+
# |DATOS DEL PROGRAMA                                        |
# +==========================================================+
# |                                                          |
# |Proyecto:       Rastreo-Tlalnepantla                      |
# |Archivo:        sms_api.py                                |
# |Descripcion:    Programa Principal de la Aplicacion       |
# |Empresa:        Tinny Development                         |
# |Desarrollador:  Ing. Agustin Noguez Salazar               |
# |                                                          |
# +==========================================================+
# |CONTROL DE VERSIONES                                      |
# +==========================================================+
# |                                                          |
# |Version:       1.1.0                                      |
# |Fecha:         14-Marzo-2017                              |
# |                                                          |
# +==========================================================+
# |POR HACER:                                                |
# +==========================================================+
# |TODO: El Endpoint debe obtenerse en base a la IP del Host |
# |TODO: Crear una función de impresión de variable y type   |
# |TODO: Reducir todo el código a 79 líneas                  |
# |TODO: Diagrama de Flujo en EdrawMax                       |
# |FIXME: Las funciones de LOG solo corren 1 vez             |
# |TODO: Algoritmo para insertar de acuerdo a fecha          |
# |TODO: Mostrar en el archivo LOG el entorno del sistema    |
# +----------------------------------------------------------+

# =====> LIBRERIAS <===== #

import datetime                     # Librería para manejo de Hora y Fecha
import logging                      # Librería para manejo de LOG
import os                           # Librería para manejo de Carpetas
import pprint                       # Librería para imprimir listas bonitas
import pymongo                      # Libreria para conexión a MongoDB
import requests                     # Librería para manejo de Peticiones
import socket                       # Librería para manejo de Hostname
import subprocess                   # Librería para manejo de SSID
import time                         # Librería para manejo de tiempo
import sys                          # Libreria para manejo de Sistema Operativo

# =====> VARIABLES GLOBALES <===== #

environment = 'production'
size_sms = '300'

log_folder = ''
year_folder = ''
month_folder = ''

Ps_Zero = "Create_Log_File()"
Ps_One = "Get_Hostname"
Ps_Two = "Set_Endpoint"
Ps_Three = "Get_SMS"
Ps_Four = "Filter_SMS_Inbox"
Ps_Five = "Filter_SMS_Desired"
Ps_Six = "Remove_SMS_Duplicates"
Ps_Seven = "Create_Final_List"
Ps_Eight = "Config_Database"
Ps_Nine = "Insert_Values"
Msg_Fail = " FAIL\n"

# =====> FUNCIONES <=====#


def Get_DateTime():
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    sys.stdout.write(timestamp)


def Print_Title(title_value):
    if title_value == 0:
        sys.stdout.write("\n==> " + Ps_Zero + " at ")
    elif title_value == 1:
        sys.stdout.write("\n==> " + Ps_One + " at ")
    elif title_value == 2:
        sys.stdout.write("\n==> " + Ps_Two + " at ")
    elif title_value == 3:
        sys.stdout.write("\n==> " + Ps_Three + " at ")
    elif title_value == 4:
        sys.stdout.write("\n==> " + Ps_Four + " at ")
    elif title_value == 5:
        sys.stdout.write("\n==> " + Ps_Five + " at ")
    elif title_value == 6:
        sys.stdout.write("\n==> " + Ps_Six + " at ")
    elif title_value == 7:
        sys.stdout.write("\n==> " + Ps_Seven + " at ")
    elif title_value == 8:
        sys.stdout.write("\n==> " + Ps_Eight + " at ")
    elif title_value == 9:
        sys.stdout.write("\n==> " + Ps_Nine + " at ")


def Log_Handler_Info(info_value):
    if info_value == 0:
        print("")
        logging.info(Ps_Zero)
    elif info_value == 1:
        logging.info(Ps_One + "(" + type_hostname + ") ==> " + hostname)
    elif info_value == 2:
        logging.info(Ps_Two + "(" + type_endpoint + ") ==> " + endpoint)
    elif info_value == 3:
        logging.info(Ps_Three + "(" + type_sms_list + ") ==> (<---" + sz_sms_list + "--->)\n\n" + pprint.pformat(sms_list) + "\n")
    elif info_value == 4:
        logging.info(Ps_Four + "(" + type_inbox_list + ") ==> (<---" + sz_inbox_list + "--->)\n\n" + pprint.pformat(inbox_list) + "\n")
        logging.info("¡Se ignoraron " + str(del_inbox_list) + " mensajes de outbox!")
    elif info_value == 5:
        logging.info(Ps_Five + "(" + type_desired_list + ") ==> (<---" + sz_desired_list + "--->)\n\n" + pprint.pformat(desired_list) + "\n")
        logging.info("¡Se ignoraron " + str(del_desired_list) + " mensajes sin latitude!")
    elif info_value == 6:
        logging.info(Ps_Six + "(" + type_reduced_list + ") ==> (<---" + sz_reduced_list + "--->)\n\n" + pprint.pformat(reduced_list) + "\n")
        logging.info("¡Se ignoraron " + str(del_reduced_list) + " mensajes viejos!")
    elif info_value == 7:
        logging.info(Ps_Seven + "(" + type_final_list + ") ==> (<---" + sz_final_list + "--->)\n\n" + pprint.pformat(final_list) + "\n")
    elif info_value == 8:
        logging.info(Ps_Eight + "\n")
    elif info_value == 9:
        logging.info(Ps_Nine + "\n")


def Log_Handler_Error(error_value):
    if error_value == 1:
        print(Ps_One + Msg_Fail)
        logging.error(Ps_One)
        exit()
    if error_value == 2:
        print(Ps_Two + Msg_Fail)
        logging.error(Ps_Two)
        exit()
    if error_value == 3:
        print(Ps_Three + Msg_Fail)
        logging.error(Ps_Three)
        exit()
    if error_value == 4:
        print(Ps_Four + Msg_Fail)
        logging.error(Ps_Four)
        exit()
    if error_value == 5:
        print(Ps_Five + Msg_Fail)
        logging.error(Ps_Five)
        exit()
    if error_value == 6:
        print(Ps_Six + Msg_Fail)
        logging.error(Ps_Six)
        exit()
    if error_value == 7:
        print(Ps_Seven + Msg_Fail)
        logging.error(Ps_Seven)
        exit()
    if error_value == 8:
        print(Ps_Eight + Msg_Fail)
        logging.error(Ps_Eight)
        exit()


def Create_Log_Folder():

    # Variables globales usadas en la función
    global log_folder

    # Process
    try:
        current_folder = os.getcwd()
        log_folder = os.path.join(current_folder, "LOGS")
        print("\n(Path)==> LOGS Folder: " + log_folder)
        log_folder_exists = os.path.exists(log_folder)
        if log_folder_exists is False:
            os.mkdir(log_folder)
    except:
        print("\n¡¡¡Error al crear LOGS Folder!!!")


def Create_Year_Folder():

    # Variables globales usadas en esta función
    global year_folder

    # Process
    try:
        year_value = datetime.datetime.now().strftime('%Y')
        year_folder = os.path.join(log_folder, year_value)
        print("\n(Path)==> Year Folder: " + year_folder)
        year_folder_exists = os.path.exists(year_folder)
        if year_folder_exists is False:
            os.mkdir(year_folder)
    except:
        print("\n¡¡¡Error al crear Year Folder!!!")


def Create_Month_Folder():

    # Variables globales usadas en esta función
    global month_folder

    # Process
    try:
        str_month_value = datetime.datetime.now().strftime('%m')
        int_month_value = int(str_month_value)
        if int_month_value == 1:
            month_value = 'Enero'
        elif int_month_value == 2:
            month_value = 'Febrero'
        elif int_month_value == 3:
            month_value = 'Marzo'
        elif int_month_value == 4:
            month_value = 'Abril'
        elif int_month_value == 5:
            month_value = 'Mayo'
        elif int_month_value == 6:
            month_value = 'Junio'
        elif int_month_value == 7:
            month_value = 'Julio'
        elif int_month_value == 8:
            month_value = 'Agosto'
        elif int_month_value == 9:
            month_value = 'Septiembre'
        elif int_month_value == 10:
            month_value = 'Octubre'
        elif int_month_value == 11:
            month_value = 'Noviembre'
        elif int_month_value == 12:
            month_value = 'Diciembre'
        month_folder = os.path.join(year_folder, month_value)
        print("\n(Path)==> Month Folder: " + month_folder)
        month_folder_exists = os.path.exists(month_folder)
        if month_folder_exists is False:
            os.mkdir(month_folder)
    except:
        print("\n¡¡¡Error al crear Month Folder!")

# Function 0:


def Create_Log_File():

    # Process
    try:
        log_file = datetime.datetime.now().strftime('%d-%m-%Y-%H%M%S.log')
        name_log_file = os.path.join(month_folder, log_file)
        print("\n(Path)==> LOG File: " + name_log_file)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%H:%M:%S',
                            filename=name_log_file,
                            filemode='w'
                            )
        Print_Title(0)
        Get_DateTime()
        Log_Handler_Info(0)
    except:
        print("\n¡¡¡Error al crear LOG File!!!")

# Process 1:


def Get_Hostname():

    # Variables globales usadas en esta función
    global hostname
    global type_hostname

    # Process
    try:
        Print_Title(1)
        Get_DateTime()
        hostname = socket.gethostname()
        type_hostname = str(type(hostname))
        print("\n\n" + type_hostname + " ==> Hostname: " + hostname)
        Log_Handler_Info(1)
    except:
        print("\n¡¡¡Error al detectar Hostname!!!")
        Log_Handler_Error(1)

# Process 2:


def Set_Endpoint():

    # Variables globales usadas en esta función
    global endpoint
    global type_endpoint

    # Process
    try:
        Print_Title(2)
        Get_DateTime()
        if(hostname == 'Anonymous'):
            endpoint = 'http://192.168.0.5:8080/v1/sms/?limit=' + size_sms
        elif(hostname == 'Anonymous-Xubuntu'):  # Dulce-Hogar
            endpoint = 'http://192.168.0.5:8080/v1/sms/?limit=' + size_sms
        elif(hostname == 'Tinnyware-ZorinOS'):  # Dulce-Hogar
            endpoint = 'http://192.168.0.5:8080/v1/sms/?limit=' + size_sms
        elif(hostname == 'Decepticon-FerenOS'):  # ATIA
            endpoint = 'http://192.168.100.233:8080/v1/sms/?limit=' + size_sms
        type_endpoint = str(type(endpoint))
        print("\n\n" + type_endpoint + " ==> Endpoint: " + endpoint)
        Log_Handler_Info(2)
    except:
        print("\n¡¡¡Error al definir Endpoint!!!")
        Log_Handler_Error(2)

# Process 3:


def Get_SMS():

    # Variables globales usadas en esta funcion
    global sms_list
    global type_sms_list
    global sz_sms_list

    # Process
    try:
        # URL de REST SMS Gateway (Se solicitan los últimos 100 mensajes)
        Print_Title(3)
        Get_DateTime()
        response = requests.get(endpoint)
        # print(response)
        response_dict = response.json()
        # print(response_dict)
        sms_list = response_dict['messages']
        type_sms_list = str(type(sms_list))
        sz_sms_list = str(len(sms_list))
        if environment == 'development':
            print("\n\n" + type_sms_list + " ==> SMS List(" + sz_sms_list + "):")
            pprint.pprint(sms_list)
            Log_Handler_Info(3)
        elif environment == 'production':
            print("\n\n" + type_sms_list + " ==> SMS List(" + sz_sms_list + "):")
            Log_Handler_Info(3)
    except:
        Log_Handler_Error(3)

# Process 4:


def Filter_SMS_Inbox():

    # Variables globales usadas en esta funcion
    global inbox_list
    global type_inbox_list
    global sz_inbox_list
    global del_inbox_list

    # Process
    try:
        Print_Title(4)
        Get_DateTime()
        inbox_list = [x for x in sms_list if x['msg_box'] == "inbox"]
        type_inbox_list = str(type(inbox_list))
        sz_inbox_list = str(len(inbox_list))
        if environment == 'development':
            print("\n\n" + type_inbox_list + " ==> Inbox List(" + sz_inbox_list + "):")
            pprint.pprint(inbox_list)
            del_inbox_list = len(sms_list)-len(inbox_list)
            print("\n¡Se ignoraron " + str(del_inbox_list) + " mensajes de outbox!")
            Log_Handler_Info(4)
        elif environment == 'production':
            print("\n\n" + type_inbox_list + " ==> Inbox List(" + sz_inbox_list + "):")
            del_inbox_list = len(sms_list)-len(inbox_list)
            print("\n¡Se ignoraron " + str(del_inbox_list) + " mensajes de outbox!")
            Log_Handler_Info(4)
    except:
        Log_Handler_Error(4)

# Process 5:


def Filter_SMS_Desired():

    # Variables globales usadas en esta funcion
    global desired_list
    global type_desired_list
    global sz_desired_list
    global del_desired_list

    # Process
    try:
        Print_Title(5)
        Get_DateTime()
        desired_list = [x for x in inbox_list if x['body'].find("lat:") == 0]
        type_desired_list = str(type(desired_list))
        sz_desired_list = str(len(desired_list))
        if environment == 'development':
            print("\n\n" + type_desired_list + " ==> Desired List(" + sz_desired_list + "):")
            pprint.pprint(desired_list)
            del_desired_list = len(inbox_list)-len(desired_list)
            print("\n¡Se ignoraron " + str(del_desired_list) + " mensajes sin latitude!")
            Log_Handler_Info(5)
        elif environment == 'production':
            print("\n\n" + type_desired_list + " ==> Desired List(" + sz_desired_list + "):")
            del_desired_list = len(inbox_list)-len(desired_list)
            print("\n¡Se ignoraron " + str(del_desired_list) + " mensajes sin latitude!")
            Log_Handler_Info(5)
    except:
        Log_Handler_Error(5)

# Process 6:


def Remove_SMS_Duplicates():

    # Variables globales usadas en esta funcion
    global reduced_list
    global type_reduced_list
    global sz_reduced_list
    global del_reduced_list

    # Process
    try:
        Print_Title(6)
        Get_DateTime()
        seen = set()
        reduced_list = ([x for x in desired_list if [(x['address']) not in seen, seen.add((x['address']))][0]])
        type_reduced_list = str(type(reduced_list))
        sz_reduced_list = str(len(reduced_list))
        if environment == 'development':
            print("\n\n" + type_reduced_list + " ==> Reduced List(" + sz_reduced_list + "):")
            pprint.pprint(reduced_list)
            del_reduced_list = len(desired_list)-len(reduced_list)
            print("\n¡Se ignoraron " + str(del_reduced_list) + " mensajes viejos!")
            Log_Handler_Info(6)
        elif environment == 'production':
            print("\n\n" + type_reduced_list + " ==> Reduced List(" + sz_reduced_list + "):")
            del_reduced_list = len(desired_list)-len(reduced_list)
            print("\n¡Se ignoraron " + str(del_reduced_list) + " mensajes viejos!")
            Log_Handler_Info(6)
    except:
        Log_Handler_Error(6)

# Process 7:


def Create_Final_List():

    # Variables globales usadas en esta función
    global final_list
    global type_final_list
    global sz_final_list

    # Process
    try:
        Print_Title(7)
        Get_DateTime()
        print("\n")
        index_list = []
        for index in range(int(sz_reduced_list)):
            address = reduced_list[index]['address']
            body = reduced_list[index]['body']
            index_init_lat = body.find("lat:")
            index_init_long = body.find("long:")
            index_init_speed = body.find("speed:")
            index_init_T = body.find("T:")
            latitude = body[index_init_lat+4:index_init_long-1]
            longitude = body[index_init_long+5:index_init_speed-1]
            year = body[index_init_T+2:index_init_T+4]
            month = body[index_init_T+5:index_init_T+7]
            day = body[index_init_T+8:index_init_T+10]
            hour = body[index_init_T+11:index_init_T+13]
            minute = body[index_init_T+14:index_init_T+16]
            datetime = body[index_init_T+2:index_init_T+16]
            index_dict = dict(address=address, datetime=datetime, latitude=latitude, longitude=longitude)
            # print(index_dict)
            index_list.append(index_dict)
            # print(index_list)
        final_list = index_list
        type_final_list = str(type(final_list))
        sz_final_list = str(len(final_list))
        if environment == 'development':
            print(type_final_list + " ==> Final List(" + sz_final_list + "):")
            pprint.pprint(final_list)
            Log_Handler_Info(7)
        elif environment == 'production':
            print(type_final_list + " ==> Final List(" + sz_final_list + "):")
            Log_Handler_Info(7)
    except:
        Log_Handler_Error(7)

# Process 8:


def Config_Database():

    # Variables globales usadas en esta función
    global collection

    # Process
    try:
        Print_Title(8)
        Get_DateTime()
        URI = "mongodb+srv://Tinny:Turner@rastreo-tlalnepantla-fdz1a.mongodb.net/2019"
        connection = pymongo.MongoClient(URI)
        database = connection['2019']
        collection = database['marzo']
        print("\n\nConexión exitosa a MongoDB")
    except:
        Log_Handler_Error(8)

# Process 9:


def Insert_Values():

    # Process
    try:
        Print_Title(9)
        Get_DateTime()
        collection.insert(final_list)
        Log_Handler_Info(9)
        print("\n\n¡Valores insertados!")
    except:
        Log_Handler_Error(9)

# Función Principal:


def Main_Function():

    # Process
    while True:
        Get_SMS()
        Filter_SMS_Inbox()
        Filter_SMS_Desired()
        Remove_SMS_Duplicates()
        Create_Final_List()
        Insert_Values()
        time.sleep(5)

Create_Log_Folder()
Create_Year_Folder()
Create_Month_Folder()
Create_Log_File()
Get_Hostname()
Set_Endpoint()
Get_SMS()
Filter_SMS_Inbox()
Filter_SMS_Desired()
Remove_SMS_Duplicates()
Create_Final_List()
Config_Database()
Insert_Values()
# Main_Function()
