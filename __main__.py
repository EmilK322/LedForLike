import settings as config
from webServer import WebServer

webServer = WebServer()

if __name__ == '__main__':
    webServer.app.run(host='0.0.0.0', port=config.WEB_PORT)
