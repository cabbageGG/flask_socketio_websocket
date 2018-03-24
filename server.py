#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/3/20 11:23'

from flask import Flask, render_template,jsonify
from flask.ext.socketio import SocketIO
import threading

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'my-project'
symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

socketio = SocketIO(app)

import redis
redis_client = redis.Redis(host='127.0.0.1', port=6379,db=0)

@app.route('/')
def get_index_page():
    return render_template('index.html')

@app.route('/subscribe')
def get_redis_price():
    socketio.emit('get price', {'data': get_redis_data()},namespace='/test')
    result = {
        'status': 'ok'
    }
    return jsonify(result)

def get_redis_data():
    names = ['G_'+i+'_1' for i in symbols] + ['G_'+i+'_2' for i in symbols] + ['G_' + i + '_time' for i in symbols] + \
            ['MRG_'+i+'_1' for i in symbols] + ['MRG_'+i+'_2' for i in symbols] + ['MRG_' + i + '_time' for i in symbols]
    data = {name:redis_client.get(name) for name in names}
    #print(data)
    return data

def subscribe(*args):
    import requests
    url = "http://127.0.0.1:5101/subscribe"
    while True:
        try:
            requests.request(method='GET', url=url)
        except Exception as e:
            print('error: %s' % e)
        import time
        time.sleep(0.2)

if __name__ == "__main__":
    t = threading.Thread(target=subscribe)
    t.start()
    socketio.run(app, host='0.0.0.0', port=5101)
