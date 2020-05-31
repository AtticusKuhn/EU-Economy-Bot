##this files is where the database stores info about money

import PyMongo
from pymongo import MongoClient


client = MongoClient('ADIPAT FILL THIS IN')
db = client.database
servers = db.servers


def send(guild, sender, recipiant, amount, wallet):
    pass

def get_balance(guild,wallet):
    pass
def alter_money(guild, amount,wallet):
    pass
def set_money(guild, amount, wallet):
    pass