from flask import Flask, request, jsonify
from talkWithMQTT import MqttWork

class WebServer:
    app = Flask(__name__)

    @app.route('/echo', methods=['GET', 'POST'])
    def api_echo():
        # get the key and value of the request
        data = {k: v for k, v in request.args.items()}
        # turn the data to json
        resp = jsonify(data)
        return resp

    # get json from request and send it to broker
    @app.route('/postjson', methods=['POST'])
    def post_json():
        if request.is_json:
            content = request.get_json()
        print(content)

        # send message to mqtt broker
        with MqttWork() as mqtt:
            mqtt.publish(topic='someTopic', message=(str(content)))

        resp = 'got from request and send to broker:\n%s' % content
        return resp

    @app.route('/')
    def api_root():
        return 'welcome'
