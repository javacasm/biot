#!/usr/bin/python
# -*- coding: utf-8 -*-

# v1.5

'''
SOLO PARA PYTHON 3.x

algunas bibliotecas que quizas necesites instalar:

(si no puedes instalar directamente intentalo mejor con 'sudo'
y si no te funciona con 'pip install' intentalo con 'pip3 install')

python -m pip install --upgrade pip setuptools wheel
python -m pip install pyserial
python -m pip install matplotlib
python -m pip install numpy
python -m pip install python-telegram-bot --upgrade

Si lo vas a ejecutar desde un ordenador con windows
quizas esta pagina te facilite la vida para instalar paquetes
https://www.lfd.uci.edu/~gohlke/pythonlibs/


'''

#--------------------------------------------------------
# IMPORTACION DE MODULOS
#--------------------------------------------------------

#




# FILTRADO DE ERRORES
#matplotlib (al menos la version que uso) me genera algunos mensajes de advertencia que prefiero no ver
import warnings
warnings.filterwarnings("ignore")

# TIEMPOS, FECHAS
# from time import sleep      #pausas...
#import datetime


#INTERACTUAR CON EL SISTEMA OPERATIVO
    
# import sys              #Conocer el tipo de sistema operativo
import time             #manejo de funciones de tiempo (fechas, horas, pausas...)
import os               #manejo de funciones del sistema operativo 
# from os import walk     #funciones para movernos por directorios



#====================================================================================================
#  INICIO DEL BLOQUE DEFINICION DE CONSTANTES Y VARIABLES GLOBALES PARA EL PROGRAMA 
#====================================================================================================

import config


#Ruta absoluta en la que se encuentra el script. Util apra las llamadas desde el inicio del sistema

nombreScriptEjecucion = os.path.basename(__file__)




print ("==================================================")
print ("\nRuta ABSOUTA DEL PROGRAMA:\n", config.ruta_programa)
print ("\nNombre del fichero en ejecucion:\n", nombreScriptEjecucion)
print ("\n==================================================\n\n")

FLAG_momento_salvado_datos = True   #para controlar el momento de salvado automatico de los datos
FLAG_backup_datos_Enabled = True    #para permitir (o no) el salvado automatico y periodico de los datos

FLAG_reinicio_Arduino = True        #control de si es la primera vez que estamos intentando acceder a arduino
                                    #para evitar errores por variables que aun no se hayan podido cargar

FLAG_estacion_online = True         #podemos desactivala si no vamos a hacer uso de telegram y correo


################   " <---------- METADATOS ------->   <------- SENSORES -------> "
cabeceraTXTdatos = "n muestra\tESTACION\tFECHA\tHORA\tTemperatura\tHumedad\tPH\tCO2\tAzul\tRojo\tPresion\tConductividad\tTemp.Liquido\tVerde"


minuto_adquisicion_datos = -1       # para forzar lectura y preparacion de datos justo al iniciar el programa, si no da error 
minuto_dibujar_grafica = -1
minuto_error_grafica = -1
minuto_error_arduino  = -1





valor_sensor_Now = []
ultimo_valor_sensor_valido = []

#variables globales para almacenar los datos recogidos de arduino
for i in range(0,10):
    valor_sensor_Now.append(0)
    ultimo_valor_sensor_valido.append(0)
    
#esta lista es muy importante ya que guardaran los datos de las muestras
# para registro y para dibujar de la grafica
lista_Datos_Experimento_Bio = []


#----------------------------------------------------------------------------------------------------
#  FIN DEL BLOQUE DEFINICION DE VARIABLES GLOBALES
#----------------------------------------------------------------------------------------------------




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

#   INICIO DEL PROGRAMA COMO TAL  (creaccion de instancia a clases y algunas otras definiciones relacionadas con los tiempos)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

import utils

#creacion de un reloj con hora local que habra que actualizar con su metodo update() cuando queramos saber la hora actual
reloj = utils.RelojLOCAL()
reloj.update()

FECHA = reloj.fecha
RELOJ = reloj.reloj
DIA = int(reloj.dia)
HORA = int(reloj.hora)
MINUTO = int(reloj.minuto)
SEGUNDO = int(reloj.segundo)



#====================================================================================================
# PUERTO SERIE PARA COMUNICACION CON ARDUINO
#====================================================================================================
# Crear una instancia de Serial para 'dialogar' con Arduino
'''
En este bloque creamos una instancia al puerto donde se conecta arduino y verificamos su validez.
Tambien se encarga de vigilar eventuales fallos de conexion y evitar los bloqueos del programa,
encargandose de gestionar la reconexion de arduino incluso aunque esta se haga en un puerto distinto
del que se conecto inicialmente
'''

import arduinoUtils

arduinoSerialPort,puertoDetectado = arduinoUtils.detectarPuertoArduino() #detactamos automaticamente el puerto

if (puertoDetectado != ''):
    # arduinoSerialPort = serial.Serial(puertoDetectado, VELOCIDAD_PUERTO_SERIE) #usamos el puerto detectado
    print ("\n ** ARDUINO CONECTADO EN " + puertoDetectado + " ** \n")

else:
    print (" == ARDUINO NO PRESENTE == ")
    print ("    conecte la estacion antes de 60 segundos\n")

    tiempoInicio = time.time()
    ActualTime = time.time()
    while (ActualTime - tiempoInicio < 60): 
        arduinoSerialPort, puertoDetectado = arduinoUtils.detectarPuertoArduino() #detactamos automaticamente el puerto
        ActualTime = time.time()
        if (puertoDetectado != ''):
            # arduinoSerialPort = serial.Serial(puertoDetectado, VELOCIDAD_PUERTO_SERIE) #usamos el puerto detectado
            print ("\n ** ARDUINO CONECTADO EN " + puertoDetectado + " ** ")
            break

if (puertoDetectado == ''):
    print ("\n == CONECTE LA ESTACION Y REINICIE EL PROGRAMA == \n")

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# =========================================================================================================
#   BUCLE PRINCIPAL  DEL PROGRAMA   (SISTEMA VEGETATIVO)
# =========================================================================================================
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm



# Bucle para realizar las mediciones, calculos asociados a ellas y representacion de las mismas en forma grafica
'''
#Si hay AUTOMATA CONECTADO creamos la grafica y resto de procesos
asociados a la adquisicion de datos y su representacion, si no, salimos

Entramos aqui solo si se ha detectado una placa arduino o compatible para la adquisicion de datos

'''
import graficos
import utils
import Datos
import TelegramUtils
import emailUtil

if puertoDetectado:  

    graficos.initPlot()
    
    #hacemos una consulta a la estacion para despertarla (por si acaso)
    try:
        arduinoUtils.consultar_Arduino(arduinoSerialPort,0.5)
    except:
        pass

    # **** ENVIO DE MENSAJE PARA NOTIFICAR AL ADMINISTRADOR DE UN REINICIO DEL SISTEMA  ****
    if FLAG_estacion_online == True and config.ADMIN_USER != None: 
        try:
            send_message ('Estacion Reiniciada\n'+nombreScriptEjecucion, ADMIN_USER)
        except:
            pass
     
    ''' Cargar datos desde backup si los hubiese para continuar un experimento en curso '''
    
    try:   
        #carga de la lista que continene los datos acumuados (grafica completa)
        file_datos_experimento = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_DATOS_EXPERIMENTO
        estado_carga, lista_Datos_Experimento_Bio = Datos.cargar_datos_desde_fichero(file_datos_experimento)
        if estado_carga == False:
            lista_Datos_Experimento_Bio = []
            print ("lista_Datos_Experimento_Bio[]  no pudo ser restaurada")
            print ("buscando copia de seguridad...")
            longitud_extension = len(file_datos_experimento.split(".")[-1])
            nombre_con_ruta_backup = file_datos_experimento[:-longitud_extension] + "bak"
            estado_carga, lista_Datos_Experimento_Bio = Datos.cargar_datos_desde_fichero(nombre_con_ruta_backup)                                                                            
            if(estado_carga==False):
                print ("ERROR CARGANDO DATOS, se reinicia la toma de datos desde cero")
                
        if(estado_carga==True):
            pass
            ultima_valida = lista_Datos_Experimento_Bio[-1]
            ultima_valida = ultima_valida[0]
            print("FECHA/HORA Ultima muestra valida: ",ultima_valida[1],ultima_valida[2])

    except:
        lista_Datos_Experimento_Bio = []
        print ("ERROR CARGANDO DATOS, se reinicia la toma de datos desde cero") 
            
                                                                                        
            
    print ("FECHA y HORA DEL REINICO DEL PROGRAMA:   ", reloj.fechayhora)
    print ("\n\n")



# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#  INICIO DE LA ADQUISICION Y REPRESENTACION      
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


    while (True):
        reloj.update()
        FECHA = reloj.fecha
        RELOJ = reloj.reloj
        DIA = int(reloj.dia)
        HORA = int(reloj.hora)
        MINUTO = int(reloj.minuto)
        SEGUNDO = int(reloj.segundo)

                    
        # ========== ADQUISICION de datos desde ARDUINO ================================================================
        try:
            if time.time() >= minuto_adquisicion_datos + config.TIEMPO_ENTRE_MUESTRAS:
                muestra_nuevo_formato = []
                #print (utils.epochDate(time.time()), "DEBUG >> peticion")
                muestra_datos = arduinoUtils.consultar_Arduino(arduinoSerialPort,.5)
                while muestra_datos == None:
                    #print (utils.epochDate(time.time()), " DEBUG >> muestra de datos NONE")
                    muestra_datos = arduinoUtils.consultar_Arduino(arduinoSerialPort,2) #si hubo fallo, damos un poco mas de tiempo en las siguientes peticiones

                if muestra_datos != None and str(type(muestra_datos)) == "<class 'list'>":
                    print (utils.epochDate(time.time()), " DEBUG >> muestra de datos: ", muestra_datos)

                    ##comprobar que la muestra es correcta  (establecer las condiciones que deseemos, mayores de un valor, menores, en un rango...)
                    if muestra_datos[0] !=None and muestra_datos[1] !=None and muestra_datos[2] !=None:
                        FLAG_reinicio_Arduino = False
                        
                        for i in range(0,10):
                            valor_sensor_Now[i] = muestra_datos[i]
                            ultimo_valor_sensor_valido[i] = muestra_datos[i]
                        
                        
                        #si hay muestra valida, Creacion de METADATOS
                        muestra_metadatos = []
                        muestra_metadatos.append(config.ID_ESTACION_BIO)  # Sustituir con un ID propio de cada estacion para que los datos
                                                            # sean siempre reconocibles aun que se trunque un archivo
                        muestra_metadatos.append(FECHA) # Insertamos los datos de fecha y hora en la lista
                        muestra_metadatos.append(RELOJ)
                        #con los metadatos creamos una lista y con los datos de los sensores otra lista
                        #con estas dos sublistas formamos una lista (muestra completa) que son los 'puntos' que iremos añadiendo
                        #Ahora la muestra es completa: [[metadatos], [Valores actuales]]
                        #Cada punto guardado es una lista donde:
                        #lista[0], son los metadatos
                        #lista[1], son los datos de los sensores
                        # De esta forma no hay problema si se añaden mas metadados o mas datos en el futuro.

                        muestra_nuevo_formato.append(muestra_metadatos)
                        muestra_nuevo_formato.append(muestra_datos)

                        #Ahora la muestra es completa: [[metadatos], [Valores actuales]]

                        #print (utils.epochDate(time.time()), " DEBUG >> muestra_nuevo_formato: ", muestra_nuevo_formato)

                        lista_Datos_Experimento_Bio.append(muestra_nuevo_formato)                  

                        #si todas las tareas se realizan correctamente, se actualiza el minuto para la proxima toma de muestras
                        #en caso contrario  en el proximo ciclo del programa se volvera a intentar otra toma de datos
                        minuto_adquisicion_datos = time.time()

                #Si se produce algun error en la adquisicion de datos, dejamos vigentes los ultimos que fueron validos
                #que NO se aplicaran a las listas, PERO sirven para no generar errores en las peticiones
                #de los usuarios que se produzcan mientras se obtienen datos correctos
                else:
                    if FLAG_reinicio_Arduino == False: #esta bandera es para evitar que se traten de conservar
                                                       #valores que no existen (en caso de reinicio)
                        for i in range(0,10):
                            valor_sensor_Now[i] = ultimo_valor_sensor_valido[i]

        except:
            if MINUTO != minuto_error_arduino:       #solo si ha pasado un minuto del ultimo error se notifica
                minuto_error_arduino = MINUTO        #refresco la referencia con el minuto actual
                print (utils.epochDate(time.time()),"ERROR en las lecturas de arduino")

 

        # ========== PREPARAR las listas de DATOS y REPRESENTARLOS EN LA GRAFICA =======================================
        try:           
            if len(lista_Datos_Experimento_Bio) > 1:
                if MINUTO != minuto_dibujar_grafica:
                    graficos.clear()

                    #podemos aprovechar la funcion de dibujado para extraer los datos de interes como max, min, medias...
                    #que por ahora no usamos para nada, pero ahí queda
                    datos_de_interes = graficos.dibujar_grafica(lista_Datos_Experimento_Bio,reloj.fecha,HORA,MINUTO)
                    
                    graficos.pausePlot(.025) # Pausa para el refresco del grafico. Es necesaria, si no, no se ve la representacion :(
                    minuto_dibujar_grafica = MINUTO
            
        except:
            print (utils.epochDate(time.time()),"ERROR al dibujar grafica")
            time.sleep(25) # pausa de 25 segundos para no llenar la pantalla de mensajes de error

                
        # ========== COPIA de SEGURIDAD de datos automaticamente cada cierto tiempo (INTERVALO_BACKUP) ==================
        try:      
            if  FLAG_backup_datos_Enabled == True and FLAG_momento_salvado_datos == True and MINUTO % config.INTERVALO_BACKUP == 0 and SEGUNDO < 20:
                ruta = config.ruta_programa + config.RUTA_BACKUP
                nombreCompletoDat = ruta + config.FICHERO_DATOS_EXPERIMENTO
                
                print (utils.epochDate(time.time())," Realizando copias de seguridad...")                
                Datos.salvar_Backup_datos(lista_Datos_Experimento_Bio, nombreCompletoDat)
                print("\t\t\tOK AUTO_BACKUP DATOS")
                
                #convertir a TXT y salvar
                nombreCompletoTxt = ruta + config.FICHERO_TXT_EXPERIMENTO
                Datos.convertir_Datos_to_TXT(lista_Datos_Experimento_Bio, nombreCompletoTxt, cabecera=cabeceraTXTdatos)
                print("\t\t\tOK AUTO_BACKUP en formato TXT")

                #guardar una copia de la representacion grafica
                nombreCompletoGrafica =  ruta + config.FICHERO_GRAFICA_EXPERIMENTO
                graficos.saveFig(nombreCompletoGrafica)
                print("\t\t\tOK AUTO_BACKUP datos graficos")
                # si la bandera se iguala a FALSE en este punto, garantizamos que todo ha salido bien
                FLAG_momento_salvado_datos = False
                
            if SEGUNDO >= 20:
                #reactivamos la bandera que permite guardar datos si el resto de condiciones son validas
                FLAG_momento_salvado_datos = True
                
        except:
            print ("---------------------------")
            print ("ERROR BACKUP_DATOS")

        # ========== ATENDER TELEGRAMAS ================================================================================ 
        if FLAG_estacion_online == True:
            try:
                #Recibir nuevos mensajes desde TELEGRAM
                TelegramUtils.atenderTelegramas()
            except:
                print ("\nERROR accediendo a telegram\n")
        # Comprobamos si tenemos alguna peticion que completar
        # ========== GESTIONAR PETICIONES  DE GRAFICA ==================================================================
            try:
                #por si alguien nos pide la grafica          
                if TelegramUtils.FLAG_enviar_PNG == True:
                    picture = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_GRAFICA_EXPERIMENTO
                    graficos.saveFig(picture)  
                    TelegramUtils.send_picture(picture)
                    TelegramUtils.FLAG_enviar_PNG = False
            except:
                print ("ERROR al generar PNG para el cliente")
                
        # ========== GESTIONAR PETICIONES  DE TXT ==================================================================
            try:
                #por si alguien nos pide la grafica          
                if TelegramUtils.FLAG_enviar_TXT == True:                      
                    doc = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_TXT_EXPERIMENTO
                    TelegramUtils.send_document(doc)
                    TelegramUtils.FLAG_enviar_TXT = False
            except:
                print ("ERROR al enviar de datos en TXT al cliente") 

            try:
                if TelegramUtils.FLAG_save_DATA == True:
                    nombre_con_ruta = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_DATOS_EXPERIMENTO
                    status1 = Datos.salvar_Backup_datos(lista_Datos_Experimento_Bio, nombre_con_ruta)
                    nombreCompleto = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_TXT_EXPERIMENTO
                    status2 = Datos.convertir_Datos_to_TXT(lista_Datos_Experimento_Bio, nombreCompleto, \
                                                         cabecera=cabeceraTXTdatos)
                    if status1==True and status2==True:
                        message = "OK, Copia de seguridad realizada"
                    else:
                        message ="ERROR. No se pudo realizar copia de seguridad"
                    TelegramUtils.send_message(message)
                    TelegramUtils.FLAG_save_DATA = False
            except:
                print("Error al salvar los datos")
            try:
                if TelegramUtils.FLAG_send_DATA == True:
                    TelegramUtils.send_message("procesando peticion...")
                    nombreRutaConExtension = config.ruta_programa + config.RUTA_BACKUP + config.FICHERO_TXT_EXPERIMENTO
                    status1 = Datos.convertir_Datos_to_TXT(lista_Datos_Experimento_Bio, nombreRutaConExtension, \
                                                     cabecera=cabeceraTXTdatos)
                    status2 = emailUtil.enviarEmail(nombreRutaConExtension)
                    if(status1==True and status2==True):
                        message ="EMAIL enviado correctamente"
                    else:
                        message ="ERROR al enviar Email. Intentalo mas tarde"
                    TelegramUtils.send_message(message)
                    TelegramUtils.FLAG_send_DATA = False
            except:
                print("Error al enviar datos")
        # ========== GESTIONAR PETICIONES  DE BORRADO DE DATOS ==================================================================
            try:
                if TelegramUtils.FLAG_enviar_INFO == True:
                    TelegramUtils.send_message ("============================\n" +
                                  "  ESTACION ID: <<" + config.ID_ESTACION_BIO + ">>\n"
                                  "  HORARIO  UTC/GMT +1\n" +
                                  "  " + reloj.fecha + "  " + reloj.reloj + "\n" +
                                  "============================\n\n" +
                                  "VALORES ACTUALES: \n\n" +
                                  " temperatura:   " + str(valor_sensor_Now[0]) + " ºC\n" +
                                  " Humedad:   " + str(valor_sensor_Now[1]) + " %\n" +
                                  " PH:   " + str(valor_sensor_Now[2])+"\n" +
                                  " CO2:   " + str(valor_sensor_Now[3]) + " ppm\n" +
                                  " Rojo:   " + str(valor_sensor_Now[4]) + " \n" +
                                  " Azul:   " + str(valor_sensor_Now[5]) + " \n" +
                                  " Verde:   " + str(valor_sensor_Now[9]) + " \n"   +
                                  " Presion:   " + str(valor_sensor_Now[6]) + " atm\n" +
                                  " Conductividad:   "+ str(valor_sensor_Now[7]) + " \n" +
                                  " Temperatura liquido:   "+ str(valor_sensor_Now[8]) + " ºC\n")
                    TelegramUtils.FLAG_enviar_INFO = False
            except:
                print("Error al enviar la info del estado actual")

        # ========== GESTIONAR PETICIONES  DE BORRADO DE DATOS ==================================================================
            try:
                #por si alguien nos pide borrar datos iniciales (antiguos)    
                if TelegramUtils.FLAG_delete_old == True:
                    if len(lista_Datos_Experimento_Bio) > 17:
                        lista_Datos_Experimento_Bio = lista_Datos_Experimento_Bio[15:]
                        message = 'Eliminados los 15 primeros datos'
                    else:
                        message = 'datos insuficuentes, intentalo mas tarde'
                    TelegramUtils.send_message (message)
                    TelegramUtils.FLAG_delete_old = False
            except:
                print ("ERROR al borrar las 15 primeras muestras")
                # muestra_nuevo_formato
            try:
                #por si alguien nos pide borrar datos finales (recientes)        
                if TelegramUtils.FLAG_delete_new == True:
                    if len(lista_Datos_Experimento_Bio) > 17:
                        lista_Datos_Experimento_Bio = lista_Datos_Experimento_Bio[:-15]
                        message = 'eliminados los ultimos 15 datos'
                    else:
                        message = 'datos insuficuentes, intentalo mas tarde'
                    TelegramUtils.send_message (message)
                    TelegramUtils.FLAG_delete_new = False
            except:
                print ("ERROR al borrar las 15 ultimas muestras")                
        graficos.pausePlot(0.05)
    graficos.closePlot()


if puertoDetectado:                               
    print ("\n> PROGRAMA TERMINADO - FIN DE ADQUISICION DE DATOS\n")

else:
    print ("     << ERROR >> MICROCONTROLADOR NO PRESENTE\n")

   


