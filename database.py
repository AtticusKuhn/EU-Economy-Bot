##this files is where the database stores info about money

import PyMongo
from pymongo import MongoClient
import pprint

client = MongoClient('ADIPAT FILL THIS IN')
db = client.database


def send(guild, from_wallet, to_wallet, amount):
    guild_collection =db[guild]
    sender_account = guild_collection.find_one(posts.find_one({"wallet": from_wallet}))
    reciever_account = guild_collection.find_one(posts.find_one({"wallet": to_wallet}))


    pass

def get_balance(guild,wallet):
    pass
def alter_money(guild, amount,wallet):
    pass
def set_money(guild, amount, wallet):
    pass