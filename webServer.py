from flask import Flask, request
from talkWithMQTT import MqttWork
import json
import time
import settings as config
from urllib import request

class WebServer:
    app = Flask(__name__)

    def get_FBname_by_Id(self , FBid: int):
        # check if we got the token from environment vars
        # if not, the token will be: ''
        if len(config.FB_ACCESS_TOKEN) > 0:
            # open the graph api url with requested id
            graph_resp = request.urlopen(config.FB_GRAPH_API_URL + str(FBid) +
                                         '?access_token=' + config.FB_ACCESS_TOKEN)
            # get the data on the page as string
            user_data = graph_resp.read()
            # convert the str data to dictionary
            user_data = user_data.decode('utf8').replace("'", '"')
            user_data = json.loads(user_data)
            # find and return the name
            if 'name' in user_data.keys():
                return user_data['name']

            # if can't find name field in the returned data from FB,
            # This can happen for several reasons:
            # the access token expired, wrong id or FB's internal problems
            else:
                return ''
        # if can't get the token from env vars
        else:
            return ''


    @app.route("/webhook", methods=['GET'])
    def verify():
        """webhook api"""
        return request.args.get('hub.challenge')

    # get json from request and send it to broker
    @app.route('/webhook', methods=['POST'])
    def post_json():
        message = {}
        if request.is_json:
            content = request.get_json()
            #print the request that came from facebook
            print('content:\n', content)

            # if the changes was the like
            if content['entry'][0]['changes'][0]['value']['item'] == 'like':
                # get the time from the request
                #converting epoch time to datetime
                epoch_time = int(content['entry'][0]['time'])
                human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
                # also get the sender id
                message = {'time': human_time,
                           'type': 'LIKE',
                           'sender_id': content['entry'][0]['changes'][0]['value']['sender_id']
                           }
                # get the user name by id
                fb_name = WebServer.get_FBname_by_Id(FBid=int(message['sender_id']))
                # if we successfully got the name
                if len(fb_name) > 0:
                    message['sender_name'] = fb_name

                # print the message that will be send to broker
                print('message:\n', json.dumps(message))

                # send message to mqtt broker
                with MqttWork() as mqtt:
                    mqtt.publish(topic=config.MQTT_FB_WEBHOOK_TOPIC_NAME, message=(json.dumps(message)))

        resp = ('got from request\n %s') % content + ('\n\nsend to broker:\n%s' % message)
        print(resp)
        return resp

    @app.route('/')
    def api_root():
        return 'welcome'
