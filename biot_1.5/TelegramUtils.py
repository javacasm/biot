# Telegram


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES TELERAM
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm



#URL de la API de TELEGRAM
URL = "https://api.telegram.org/bot{}/".format(config.TOKEN)


update_id = None

user_keyboard = [['/info','/fig'],['/email', '/txt'],['/save','/ayuda'],['/deleteOld','/deleteNew']]
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)

""" poner en marcha el bot """
telegram_bot_experimento_bio = telegram.Bot(config.TOKEN)

#comandos a mostrar al pedir '/ayuda'
listaComandos = ["/ayuda - Mostrar esta Ayuda", \
                 "/email - envia datos completos por email",\
                 "/info - Mostrar datos actuales", \
                 "/txt - envia datos completos a telegram", \
                 "/fig - Grafico de Evolucion",\
                 "/deleteOld - Borra los 15 primeros datos",\
                 "/deleteNew - Borra los 15 ultimos datos",\
                 "/save - Realiza una copia de seguridad","\n"]


#bucle para generar el texto encadenando todos los comandos de ayuda.
#Para el mensaje que se envia por telegram al pedir '/ayuda'
listaComandosTxt = ""
for comando in listaComandos:
    listaComandosTxt += comando+"\n"



def get_url(url):
    '''
    Funcion de apoyo a la recogida de telegramas,
    Recoge el contenido desde la url de telegram
    '''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def send_message(text, chat_id):
    '''
    Funcion para enviar telergamas atraves de la API
    '''
    try:
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        get_url(url)
    except:
        print("ERROR de envio")

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def atenderTelegramas(bot):
    '''
    Funcion principal de la gestion de telegramas.
    Los atiende y procesa, ejecutando aquellos que son ordenes directas.
    Solicita la 'ayuda' de otras funciones para aquellos comandos
    complejos que contiene parametros
    '''
    global text, chat_id, chat_time, comando, chat_user_name
    global FLAG_enviar_PNG, FLAG_pruebas, FLAG_enviar_TXT, FLAG_delete_old, FLAG_delete_new

    global update_id
    chat_id = 0
    try:    
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=0): #timeout=5, si nos da problemas con internet lento
            update_id = update.update_id +1

            if update.message:  # porque se podrian recibir updates sin mensaje...
                comando = update.message.text  #MENSAJE_RECIBIDO
                chat_time = update.message.date
                user = update.message.from_user #USER_FULL
                chat_id = int(update.message.from_user.id)
                chat_user_name = user.first_name #USER_REAL_NAME
                usuario = chat_user_name
                            
                try:
                    # para DEBUG, imprimimos lo que va llegando
                    print (str(chat_time) + " >>> " + str(chat_id) +": " + usuario + " --> " + comando)
                    
                    if update.message.entities[0].type == "bot_command" and update.message.text == "/start":
                        update.message.reply_text("Bienvenido a Experimento Bio v1.0", reply_markup=user_keyboard_markup)
                                            
                    # ===============   INTERPRETAR LOS COMANDOS QUE LLEGAN Y ACTUAR EN CONSECUENCIA   ===============
                    
                    if comando == "/send" and (chat_id == ADMIN_USER or ADMIN_USER == None):  #decidir quien puede enviar correos
                        send_message("procesando peticion...", chat_id)
                        nombreRutaConExtension = RUTA_PROGRAMA + RUTA_BACKUP + FICHERO_TXT_EXPERIMENTO
                        status1 = convertir_Datos_to_TXT(lista_Datos_Experimento_Bio, nombreRutaConExtension, \
                                                         cabecera=cabeceraTXTdatos)
                        status2 = enviarEmail(nombreRutaConExtension)
                        if(status1==True and status2==True):
                            send_message("EMAIL enviado correctamente", chat_id)
                        else:
                            send_message("ERROR al enviar Email. Intentalo mas tarde", chat_id)
                        return
          
                    if comando == "/save" and (chat_id == ADMIN_USER or ADMIN_USER == None):  #solo el administrador puede forzar el salvado de datos no programado
                        nombre_con_ruta = RUTA_PROGRAMA + RUTA_BACKUP + FICHERO_DATOS_EXPERIMENTO
                        status1 = salvar_Backup_datos(lista_Datos_Experimento_Bio, nombre_con_ruta)
                        nombreCompleto = RUTA_PROGRAMA + RUTA_BACKUP + FICHERO_TXT_EXPERIMENTO
                        status2 = convertir_Datos_to_TXT(lista_Datos_Experimento_Bio, nombreCompleto, \
                                                         cabecera=cabeceraTXTdatos)

                        if status1==True and status2==True:
                            send_message("OK, Copia de seguridad realizada", chat_id)
                        else:
                            send_message("ERROR. No se pudo realizar copia de seguridad", chat_id)
                        return

                    # Lista de comandos para usuarios basicos (clientes)           
                    if comando == "/ayuda":
                        send_message (listaComandosTxt, chat_id)
                        return
                    
                    if comando == "/info":
                        send_message ("============================\n" +
                                      "  ESTACION ID: <<" + ID_ESTACION_BIO + ">>\n"
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
                                      " Temperatura liquido:   "+ str(valor_sensor_Now[8]) + " ºC\n"
                                      , chat_id)
                        
                        return
                        
                       

                    if comando == "/fig":
                        FLAG_enviar_PNG = True
                        return 
                    
                    if comando == "/txt":
                        FLAG_enviar_TXT = True
                        return
                     
                    if comando == "/deleteOld" and (chat_id == ADMIN_USER or ADMIN_USER == None):
                        FLAG_delete_old = True
                        return
                    if comando == "/deleteNew" and (chat_id == ADMIN_USER or ADMIN_USER == None):
                        FLAG_delete_new = True
                        return                    
                except:
                    print ("----- ERROR ATENDIENDO TELEGRAMAS ----------------------")                      
                if chat_id != 0:
                    #ante cualquier comando desconocido devolvemos 'ok', para despistar a los que intenten 'probar suerte'
                    send_message ("OK" ,chat_id)  
        
    except:
        pass
    
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
    