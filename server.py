import os

from flask import Flask, render_template,url_for, jsonify, request
import json
from threading import Thread
from flask_cors import CORS
app = Flask(__name__)

import discord

from database import send
from methods import get_wallet

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
            account["id"]=str(account["id"])
        return str(accounts)

    @app.route('/send', methods=["POST"])
    def send_api():
        data = request.json
        print(data)
        guild = discord.utils.find(lambda m: int(m.id) == int(data["guild"]), bot.guilds)
        #member = discord.utils.find(lambda m: m.id == data.person_id, guild.members)
        res =send(int(data["person_id"]), guild, data["from_wallet"], data["to_wallet"], data["amount"])
        guild_collection =db[str(guild.id)]
        new_found_id = get_wallet(guild,data["to_wallet"])[1].id
        print(new_found_id,"new_found_id")
        new_wallet=guild_collection.find_one({"id":new_found_id})
        print(new_wallet,"new_wallet")
        del new_wallet["_id"]
        return {
            "success":res[0],
            "message":res[1],
            "new_balance":new_wallet
        }
    app.run(host='0.0.0.0', port=8080, threaded = True)

#if __name__ == '__main__':
 # 
#def run():
#    app.run(host="0.0.0.0", port=8080)
def start_server(bot):
    server = Thread(target=run,args=(bot,) )
    server.start()