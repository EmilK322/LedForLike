from flask import Flask , request , json , jsonify
import os
app = Flask(__name__)


@app.route('/echo', methods = ['GET', 'POST'])
def api_echo():
    # get the key and value of the request
    data = {k: v for k, v in request.args.items()}
    # turn the data to json
    resp = jsonify(data)
    return resp


@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)
    content = jsonify(content)
    return content



@app.route('/')
def api_root():
    #return 'to get your request in JSON, enter "/echo?param=value" '
    return 'welcome'

WEB_PORT = int(os.environ.get('PORT' , 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=WEB_PORT)