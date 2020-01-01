# Configuracion

import os               #manejo de funciones del sistema operativo 

# v1.5


'''***********************************************************************************************'''
'''***********************************************************************************************'''
'''***********************************************************************************************'''

#    IMPORTANTE, DATOS A CONFIGURAR POR EL USUARIO    #

'''***********************************************************************************************'''

#DATOS DEL SERVIDOR DE CORREO PARA REALIZAR LOS ENVIOS
#ojo, aqui estaran visibles la direccion y la contraseña :(  (Recuerdado a la hora de pasar el codigo a alguien)
#Las cuentas de gmail deberan configurarse para que admitan "dispositivos no seguros" 

SMTP_CORREO_ENVIOS = 'smtp.yandex.com'
EMAIL_CORREO_ENVIOS = 'biotecnoencuentro2019@yandex.com'
PASS_CORREO_ENVIOS = 'srgmbvdnahchrwjv'
REMITENTE_CORREO_ENVIOS = 'biotecnoencuentro2019@yandex.com'  #yandex no permite otro remitente que no sea la direccion de salida
                                                              #si usais gmail como smtp, podeis poner una cadena de texto a vuestro gusto :)

#lista de direcciones de correo a la que se enviaran los datos del experimento. Necesaria al menos una direccion.
lista_correo_experimento = ['javacasm@gmail.com']      #quitar esta y poner la vuestra


#CLAVE para la API de telegram (token del bot)
TOKEN = "892980687:AAEAr6zBV5GDFoGKhxzEjzz-yUMPmvNRV1Y" # quitar este y poner el de vuestro bot


# Definimos la id del que sera el usuarios administrador y que dispondra de derechos de uso completo
# (podemos definir otros usuarios que no tengan acceso total)

ADMIN_USER = None  #None: todos los que se conectan pueden realizar: - el envio de correo a la lista de autorizados
                   #                                                 - el salvado manual de datos
                   #                                                 - el borrado de datos
                   #Si establecemos un numero ID de telegram, solo el usuario con ese numero ID puede realizar esos tres comandos


ID_ESTACION_BIO = "BIO_JAVACASM"   # este ID se incorpora a los mensajes de informacion
                                 #y a las muestras de datos del fichero txt (sustituirla por algo personal)

TIEMPO_ENTRE_MUESTRAS = 60 # tiempo en segundos. Por defecto 60, un minuto




'''***********************************************************************************************'''
'''***********************************************************************************************'''
'''***********************************************************************************************'''

ruta_programa = os.path.dirname(os.path.abspath(__file__)) +'/'

RUTA_BACKUP = ''  #RUTA_BACKUP = 'backup/'

FICHERO_DATOS_EXPERIMENTO = 'experimento_bio.dat'
FICHERO_TXT_EXPERIMENTO = 'experimento_bio.txt'
FICHERO_GRAFICA_EXPERIMENTO = 'experimento_bio.png'


SerialDelay = 0.5                   #tiempo entre llamadas del puerto (en segundos), para que pueda reaccionar.
                                    #No usar tiempos inferiores a 0.25 segundos 
VELOCIDAD_PUERTO_SERIE = 115200

INTERVALO_BACKUP = 10               #intervalo en minutos para copias de seguridad

# MQTT configuration

MQTT_SERVER = '192.168.1.200'

BaseTopic_sub = 'MeteoSalon'