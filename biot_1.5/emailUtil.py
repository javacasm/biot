# Email



# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# ENVIO DE EMAIL
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

def enviarEmail(nombreRutaConExtension):
    '''
    Funcion para realizar los envio de los datos del experimento por email
    a los clientes suscritos
    Aqui llega la ruta + nombre del fichero registro + extrension *.txt
    Entre las tareas a realizar extraemos solo el "nombre.txt"
    para usarlo como texto en el asunto del mensaje
    '''

    global config.lista_correo_experimento
    #Esta lista contiene objetos tipo cartero,
    #con la id de telegram  .user  y las direcciones de correo .email
    #desgranamos la lista para hacer una nueva lista de solo direcciones de email
    
    destinatarios = []
    for email in config.lista_correo_experimento:
        destinatarios.append(email)
        
    nombreRutaTxt= nombreRutaConExtension
    soloNombreTxt = nombreRutaTxt.split("/")[-1]

    #el mail sale desde el correo xxxxx@xxxx.xxx (definimos el correo del remitente)
    remitente = config.REMITENTE_CORREO_ENVIOS
    # Definimos los detalles del servisor email SMTP
    smtp_server = config.SMTP_CORREO_ENVIOS
    smtp_user   = config.EMAIL_CORREO_ENVIOS
    smtp_pass   = config.PASS_CORREO_ENVIOS

    try: 
        # Construimos el mail
        msg = MIMEMultipart() 
        msg['Bcc'] = ", ".join(destinatarios)
        msg['From'] = remitente
        msg['Subject'] = 'Registro Datos   >>> ' + soloNombreTxt

        #cuerpo del mensaje en HTML
        msg.attach(MIMEText('<h1>Registro de datos de Experimento Bio</h1><p>','html'))

        ##cargamos el archivo a adjuntar
        fp = open(nombreRutaTxt,'rb')
        adjunto = MIMEBase('multipart', 'encrypted')
        #lo insertamos en una variable
        adjunto.set_payload(fp.read()) 
        fp.close()  
        #lo encriptamos en base64 para enviarlo
        encoders.encode_base64(adjunto) 
        #agregamos una cabecera e indicamos el nombre del archivo
        adjunto.add_header('Content-Disposition', 'attachment', filename=soloNombreTxt) #
        #adjuntamos al mensaje
        msg.attach(adjunto) 

        # inicializamos el stmp para hacer el envio
        server = smtplib.SMTP(smtp_server)
        server.starttls() 

        #logeamos con los datos ya seteamos en la parte superior
        server.login(smtp_user,smtp_pass)

        #realizamos los envios a los suscriptores
        server.sendmail(remitente, destinatarios, msg.as_string())
        
        #apagamos conexion stmp
        server.quit()
        print ("DEBUG >>>   CORREOS ENVIADOS")
        return True

    except Exception as e:
        print ("---------------------------")
        print ("ERROR AL ENVIAR E-MAIL")
        print(e)
        return False
