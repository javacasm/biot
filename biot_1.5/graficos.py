# Graficos


# REPRESENTACION GRAFICA DE DATOS
import matplotlib                               #funcionalidad para representacion grafica de datos
import matplotlib.pyplot as plt                 #por comodidad al llamar esta funcionalidad
from matplotlib.ticker import MultipleLocator   #para crear leyendas en los graficos


# FUNCIONES MATEMATICAS AVANZADAS
import numpy as np
import math

import time

import utils

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# REPRESENTACION GRAFICA
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

fig = None

def clear():
    plt.clf() # esto limpia la información del  área donde se pintan los graficos.

def saveFig(ficheroImagen):
    plt.savefig(ficheroImagen)

def closePlot():
    plt.close('all') 

def pausePlot(tiempo):
    plt.pause(tiempo)  ## refresco continuo del area de la grafica.

def initPlot():
        # Se prepara la zona de trabajo de la grafica 
    plt.ion() # declaramos la sesión como interactiva
    global fig
    fig = plt.figure()

def addGrafico( altura,color,columna,nombre,puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos):
    try:
        global fig
        ax = fig.add_subplot(altura)  
        plt.grid(True, lw = 0.5, ls = '--', c = '.75')
        
        plt.plot(puntos_eje_x, datos_por_sensor_y[columna], lw = 1.5, c = color)   

        plt.ylabel(nombre)
        plt.xticks(orden,etiqueta, size = 'small', color = 'b') #si comentamos esta linea aparecen como etiqueta el numero de muestra
        plt.ylim(minimos_maximos[columna][0] - 5, minimos_maximos[columna][1] + 5)

        spacing = 10 # This can be your user specified spacing. 
        minorLocator = MultipleLocator(spacing)

        # Set minor tick locations.
        ax.yaxis.set_minor_locator(minorLocator)
        # Set grid to use minor tick locations. 
        ax.grid(which = 'minor')
    except Exception as ex :
        print ("Error Dibujando grafica " + nombre)
        print(ex)
        
def dibujar_grafica(datos_brutos_experimento,fecha, hora, minuto):
    '''
    Funcion para realizar la representacion de la grafica con los datos que se van adquiriendo de ARDUINO
    Esta sera la grafica que visualizamos en la maquina en la que se ejecuta el bot
    y que enviaremos a los clientes cuando nos la soliciten.
    Esta grafica representa siempre las ultimas 24 horas
    Tambien en esta funcion nos encargamos de realiazar los calculos (max, min...).
    recibe una lista que contiene elementos que a su vez son listas/tuplas con todos los datos de interes:

    '''
    global fig 
    try:
        
        print (utils.epochDate(time.time()), " DEBUG >> dibujando grafica")
        if(len(datos_brutos_experimento) >1440):
            datos_brutos_experimento = datos_brutos_experimento[-1440:]
        # [ [              1               ], [              2               ], ....]   
        # [ [[metadatos1],[datos sensores1]], [[metadatos2],[datos sensores2]], ]
        # [metadatos] = ID, FECHA, RELOJ >> 2019_05_11 19:38:02
        # [datos sensores] = [sensor1, sensor2....]  
        
        #horas para las etiquetas de la grafica
        horas = [elemento[0][2][:2]for elemento in datos_brutos_experimento] #recortamos para dejar solo las horas

        #datos de sensores para los ejes Y        
        n_muestras = len(datos_brutos_experimento)

        #creamos una lista de listas (una por cada sensor)
        datos_por_sensor_y = [] #[[lista_sensor1], [lista_sensor2]...], una lista por cada sensor

        #extraemos los datos de los sensores: datos_brutos_experimento[n][1] (dejamos de lado los metadatos)
        datos_sensores = [elemento[1]for elemento in datos_brutos_experimento]
        
        #ahora generamos una lista con los datos de cada sensor de forma individual
        for n in range (len(datos_sensores[0])):
            lista_por_sensor = [elemento[n]for elemento in datos_sensores]
            datos_por_sensor_y.append(lista_por_sensor)
        
        # print (epochDate(time.time()), " DEBUG >> datos_por_sensor_y "+str(datos_por_sensor_y))


    except:
        print ("--------------------------------------")
        print ("ERROR al asignar datos para la grafica")
        return (False)    
    
    try:

        # //---------------------------------------------------------------\\
        #      -- Preparacion de datos para las representaciones graficas--      
        # //---------------------------------------------------------------\\
        

        
        #generacion de lista de valores eje x
        index  = 0
        puntos_eje_x=[]
        while index < n_muestras:
            #creamos una lista que seran los indices de muestra, para poner en el eje x de la grafica
            puntos_eje_x.append(index) #lista para los datos que se representaran en el eje x
            index  += 1 #incrementamos el indice para recorrer las listas
            
        #aprovechamos este punto para obtener el valor min y max de cada sensor
        # que nos sera util para establecer los rangos al dibujar la grafica
        minimos_maximos = []
        lineas_medias = []
        for n in range(len(datos_por_sensor_y)):
            dato_min = (min(datos_por_sensor_y[n]))
            dato_max = (max(datos_por_sensor_y[n]))
            #cada valos añadico sera una lista con dos valores, (el min y el max de cada sensor)
            minimos_maximos.append([dato_min, dato_max])
        
        orden=[]        #lista para almacenar la posicion de las etiquets horarias
        etiqueta=[]     #lista que contendra las etiquetas horarias de la grafica
         
        #SECCION PARA EL ETIQUETADO HORARIO DEL EJE X
        etiquetaEnCurso = -1 #como primera etiqueta ponemos una hora fuera del rango posible 
        muestrasHoraEnCurso = 0
        #recorremos  toda la lista de horas buscando un cambio
        for n in range (0,n_muestras):               # valores de (0 a n_muestras-1)
            if horas[n] != etiquetaEnCurso:          # ante una hora nueva en la lista de horas...
                etiquetaEnCurso = horas[n]           # actualizamos la etiqueta en curso para la comparacion de la busqueda 
                etiqueta.append(etiquetaEnCurso)     # almacenamos la nueva etiqueta que acabamos de localizar  
                orden.append(n)                      # y su posicion
                muestrasHoraEnCurso = n_muestras - n # localizado el ultimo cambio de hora,
                                                     # las muestras que queden son las de la hora en curso
        # Titulo de la ventana
        plt.title('Captura de datos Experimento BIO 2020, v1.5')
        fig.canvas.set_window_title('Orignal by INOPYA')
        
        addGrafico(911,'red',0,'Temp',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(912,'green',1,'Humedad',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(913,'pink',6,'Presion',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(914,'blue',2,'pH',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(915,'black',3,'CO2',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(916,'yellow',4,'Red Led',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(917,'orange',5,'Blue Led',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(918,'gray',7,'Temp. L.',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)
        addGrafico(919,'purple',8,'Conduct',puntos_eje_x, datos_por_sensor_y,etiqueta,orden,minimos_maximos)

        label_eje_x = 'MUESTRA:  ' +str(len(datos_brutos_experimento)) +' (' + str(muestrasHoraEnCurso)+')' + \
        '   FECHA:  ' + fecha + '     HORA LOCAL:  ' + ('00'+str(hora))[-2:] + ':' +('00'+str(minuto))[-2:]

        plt.xlabel(label_eje_x) #comun para los dos subplots

        datos_singulares = minimos_maximos
        
        return datos_singulares
          
    except Exception as ex :
        print ("Error Dibujando grafica")
        print(ex)
        return(False)
