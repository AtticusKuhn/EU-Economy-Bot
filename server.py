import os

from flask import Flask, render_template,url_for, jsonify, request
import json
from threading import Thread
from flask_cors import CORS
app = Flask(__name__)

import discord

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database
def run(bot):
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/servers')
    def get_servers():
        return str(db.collection_names())

    @app.route('/<guild>/wallets')
    def all_wallets(guild):
        guild_collection =db[str(guild)]
        accounts = list(guild_collection.find({"type":"personal"}))
        #accounts.append(list(guild_collection.find({"type":"role"})))
        for account in accounts:
            del account['_id']
        return str(accounts)

    @app.route('/send', methods=["POST"])
    def send_api():
        data = request.json
        member = discord.utils.find(lambda m: m.id == person_id, guild.members)
        member = discord.utils.find(lambda m: m.id == person_id, guild.members)

        return data
    app.run(host='0.0.0.0', port=8080, threaded = True)

#if __name__ == '__main__':
 # 
#def run():
#    app.run(host="0.0.0.0", port=8080)
def start_server(bot):
    server = Thread(target=run,args=(bot,) )
    server.start()