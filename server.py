from flask import Flask, render_template,url_for, jsonify
import json
from threading import Thread

#import evaluator
#import test
import logging
from flask_cors import CORS


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello World!'

#if __name__ == '__main__':
 # app.run(host='0.0.0.0', port=8080, threaded = True)
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()