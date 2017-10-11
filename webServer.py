from flask import Flask, request, jsonify


class WebServer:
    app = Flask(__name__)

    @app.route('/echo', methods=['GET', 'POST'])
    def api_echo():
        # get the key and value of the request
        data = {k: v for k, v in request.args.items()}
        # turn the data to json
        resp = jsonify(data)
        return resp

    @app.route('/postjson', methods=['POST'])
    def post_json():
        print(request.is_json)
        content = request.get_json()
        print(content)
        content = jsonify(content)
        return content

    @app.route('/')
    def api_root():
        # return 'to get your request in JSON, enter "/echo?param=value" '
        return 'welcome'
