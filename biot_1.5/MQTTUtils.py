# MQTT utils

import paho.mqtt.client as mqtt # Import the MQTT library
import config
import utils

MQTTData = { 'initTime' : [utils.getStrDateTime() , utils.getStrDateTime()] }

# Our "on message" event
def checkMQTTSubscription (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    #if topic.startswith(topic_sub):
    #    pass ## TODO: check topics
    MQTTData[topic] = [ utils.getStrDateTime() , message]
    
    utils.myLog('MQTT: '+utils.getStrDateTime() + ' ' +topic + ' - ' + message)
    
def initMQTT():
    global ourClient
    ourClient = mqtt.Client("CBT_bot_mqtt") # Create a MQTT client object with this id
    ourClient.connect(config.MQTT_SERVER, 1883) # Connect to the test MQTT broker
    utils.myLog('Conectado a MQTT broker ' + config.MQTT_SERVER)
    ourClient.subscribe(config.BaseTopic_sub+'/#') # Subscribe to the topic 
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.loop_start() # Start the MQTT client
    utils.myLog('MQTT client started')