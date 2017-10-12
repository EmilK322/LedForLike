import paho.mqtt.client as mqtt
import settings as config


class MqttWork:
    # result code values of connect method
    rc_values = {
        0: 'Connection successful',
        1: 'Connection refused - incorrect protocol version',
        2: 'Connection refused - invalid client identifier',
        3: 'Connection refused - server unavailable',
        4: 'Connection refused - bad username or password',
        5: 'Connection refused - not authorised',
        'else': 'Currently unused'}

    # prints the connection state
    def on_connect(client, userdata, flags, rc):
        if rc in MqttWork.rc_values.keys():
            print("Connected to broker with result code " + str(rc) + ': ' + MqttWork.rc_values[rc])
        else:
            print("Connected to broker with result code " + str(rc) + ': ' + MqttWork.rc_values['else'])

    # prints the publishing state
    # if this method runs, it means that the
    # message come to broker because we set qos=1
    def on_publish(client, obj, mid):
        # if message id equals to (qos==1)
        # it means that message arrived to broker
        if mid == 1:
            print("published message id: " + str(mid) + ' ---> ' + 'published message successfully arrived to broker')
        else:
            print("published message id: " + str(mid) + ' ---> ' + "published message don't arrived to broker")


    # called when instantiated
    def __init__(self):
        self.mqttc = mqtt.Client()
        # give callback methods for checking state after each action
        print('set event callbacks')
        self.mqttc.on_connect = MqttWork.on_connect
        self.mqttc.on_publish = MqttWork.on_publish

        # set the username and the password
        self.mqttc.username_pw_set('oksyyxcw', 'nv5t8VokNjP3')
        #self.mqttc.username_pw_set(config.MQTT_USER, config.MQTT_PWD)
        try:
            # trying to connect to broker
            print('run connect')
            self.mqttc.connect('m13.cloudmqtt.com', 15829)
            #self.mqttc.connect(config.MQTT_HOST, config.MQTT_PORT)

            # start threaded network loop, network loops needed to run events callbecks
            self.mqttc.loop_start()

        except ValueError:
            print("can't connect to " + 'm13.cloudmqtt.com')
            #print("can't connect to " + config.MQTT_HOST)

    # called when instance is instantiated with 'with' clause
    def __enter__(self):
        return self

    # Publish a message
    def publish(self, topic, message):
        # publish to broker, with qos==0 can check if message leave us,
        # with qos==(1 or 2) can check if message has come to broker
        print('run publish')
        self.mqttc.publish(topic=topic, payload=message, qos=1)

    # called when instance that instantiated with 'with' clause deleted
    def __exit__(self, exc_type, exc_value, traceback):
        # stop the network loop
        self.mqttc.loop_stop(force=False)
