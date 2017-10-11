import paho.mqtt.client as mqtt
import settings as config
import json
# from urllib.parse import urlparse


class MqttWork:

    def __init__(self):
        self.mqttc = mqtt.Client()

        self.mqttc.username_pw_set('oksyyxcw', 'nv5t8VokNjP3')
        #self.mqttc.username_pw_set(config.MQTT_USER, config.MQTT_PWD)
        try:
            self.mqttc.connect('m13.cloudmqtt.com', 15829)
            #self.mqttc.connect(config.MQTT_HOST, config.MQTT_PORT)
        except ValueError:
            print("can't connect to " + 'm13.cloudmqtt.com')
            #print("can't connect to " + config.MQTT_HOST)
    '''
    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
    url = urlparse.urlparse(url_str)
    topic = url.path[1:] or 'test'
    '''

    # Connect
    '''
    print(config.MQTT_USER , '--->' , config.MQTT_PWD)
    print(config.MQTT_HOST , '--->' , config.WEB_PORT)
    '''

    # Publish a message
    def publish(self, topic, message):
        self.mqttc.publish(topic=topic, payload=message)

    # Continue the network loop, exit when an error occurs
    '''
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))
    '''
