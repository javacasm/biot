# Datos



# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES CONTROL Y GESTION DE FICHEROS DE DATOS
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
   
def salvar_Backup_datos(informacion_para_salvar, nombre_con_ruta):
    ''' Salvado de datos que autogenera una copia con el mismo nombre recibido pero con extension BAK '''
    
    try:   
        ficheroDatos = open(nombre_con_ruta, "wb")
        pickle.dump(informacion_para_salvar, ficheroDatos, protocol=-1) # -1, seleccion automatica del más alto disponible  
        ficheroDatos.close()
        
        #CREACION DE COPIAS  .bak AUTOMATICAMENTE
        #separamos el nombre y la extenxion de la informacion que llega a la funcion
        longitud_extension = len(nombre_con_ruta.split(".")[-1])
        nombre_con_ruta_backup = nombre_con_ruta[:-longitud_extension] + "bak"
        ficheroDatos_backup = open(nombre_con_ruta_backup, "wb")
        pickle.dump(informacion_para_salvar, ficheroDatos_backup, protocol=-1) # -1, seleccion automatica del más alto disponible  
        ficheroDatos.close()
        return(True)

    except:
        print ("---------------------------")
        print ("Error Guardando backup >> ", nombre_con_ruta)

        return(False)                   
    
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def cargar_datos_desde_fichero(nombre_con_ruta):
    ''' Recuperacion de los datos de backup desde fichero en los momentos de reinicio '''

    datos = []
    try:
        nombreDatosFile = nombre_con_ruta
        ficheroDatos = open(nombreDatosFile,"rb")
        datos = pickle.load(ficheroDatos)
        ficheroDatos.close()
        return True, datos
        
    except:
        print ("---------------------------")
        print ("error con la carga de registros de backup")
        return False , []

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def ListaUnica (lista, destino):
    for n in range(len(lista)):
        if isinstance(lista[n],list):
            ListaUnica(lista[n], destino)
        else:
            destino.append(lista[n])
    return destino
    
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def convertir_Datos_to_TXT(datos, nombreDatosFile, cabecera=""):
    '''
    RECIBE UNA LISTA o UN EMPAQUETADO (una lista de listas) y el nombre con el que queremos guardar el TxT
    Funcion para la conversion de los datos de una serie de listas
    a un formato de texto plano separado en colunmas.
    Opcionalmente podemos indicar uan cabecera de texto apra dichos datos
    Esta sera informacion que se envia por email a los suscriptores
    '''
    #datos = lista simple  o bien lista de listas
    nombreFileSalida = nombreDatosFile

    numeroDatos = len(datos)

    outfile = open(nombreFileSalida, 'w') # Indicamos el valor 'w' para escritura.

    if cabecera != "": #si hay informacion de cabecera se añade antes de los datos para no numerar esa linea
        outfile.write(cabecera)
        outfile.write("\n\n")
        #y dejamos el fichero abierto para seguir escribiendo la informacion correspondiente a los datos

    if datos == []: #Si llega una lista vacia (que puede ser) se generarian errores,
                    #asi que añadimos una linea para informar de ello, cerramos el fichero y salimos
        outfile.write("\nNo hay informacion disponible\n")
        outfile.close()
        return (True)
    
    try:
        for x in range(len(datos)):
            lista_unica=[]
            indice = "00000"+ str(x)
            indice = indice[-5:]
            linea = indice + "\t"

            lista_unica = ListaUnica(datos[x], lista_unica)

            for elemento in lista_unica:
                if str(type(elemento))== "<class 'int'>" or str(type(elemento))== "<class 'float'>":
                    dato = float(elemento)
                    dato = "%.2f" % (dato)
                    linea += str(dato) + "\t"
                else:
                    linea += elemento + "\t"
            linea += "\n" 
            outfile.write(linea)
        outfile.close()
        return (True)

    except:
        print ("---------------------------")
        outfile.close()                         #Cerramos por si se quedo abierto
        outfile = open(nombreFileSalida, 'wb')  #Reabrimos nuevamente y escribimos un mensaje de error
        linea = "\n\nHubo un error en la conversion de datos\n\nContacte EXPERIMENTO BIO en telegram con el comando /DATA_ERROR_"+nombreDatosFile[:-4]+" y solicite los datos en formato RAW si lo desea \n" 
        outfile.write(linea)
        outfile.close()
        return (False)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  
