import os

from flask import Flask, render_template,url_for, jsonify
import json
from threading import Thread
from flask_cors import CORS

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/servers')
def get_servers():
    return str(db.collection_names())
@app.route('/<guild>/wallets')
def all_wallets(guild):
    guild_collection =db[str(guild)]
    accounts = list(guild_collection.find({}))
    return str(accounts)


#if __name__ == '__main__':
 # app.run(host='0.0.0.0', port=8080, threaded = True)
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()