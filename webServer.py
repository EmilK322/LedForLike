from flask import Flask, request, jsonify
from talkWithMQTT import MqttWork
import settings as config

class WebServer:
    app = Flask(__name__)

    @app.route("/webhook", methods=['GET'])
    def verify():
        """webhook api"""
        return request.args.get('hub.challenge')

    # get json from request and send it to broker
    @app.route('/webhook', methods=['POST'])
    def post_json():
        if request.is_json:
            content = request.get_json()
        print(content)

        # send message to mqtt broker
        with MqttWork() as mqtt:
            mqtt.publish(topic=config.MQTT_FB_WEBHOOK_TOPIC_NAME, message=(str(content)))

        resp = 'got from request and send to broker:\n%s' % content
        return resp

    @app.route('/')
    def api_root():
        return 'welcome'
