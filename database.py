##this files is where the database stores info about money





#general form of a wallet will be
#{
#   "name"   :"eulerthedestroyer",
#   "id"     :464954455029317633,
#   "type"   :"personal",
#   "balance": 5
#}
#import PyMongo
import os
from pymongo import MongoClient
import pprint
import methods
from config import config

os.system("pip install dnspython")


#import dnspython 

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database


def send(client, guild_id, from_wallet, to_wallet, amount, person):
    if not methods.can_access_wallet(client, guild_id, person, from_wallet):
        return (False, "cannot access wallet")
    try:
        amount = int(amount)
    except:
        return (False,"invalid amount" )
    guild_collection =db[str(guild_id)]
    from_wallet_id = methods.get_wallet(client, guild_id, from_wallet)
    to_wallet_id =methods.get_wallet(client, guild_id, to_wallet)
    print(to_wallet_id,from_wallet_id)
    if(from_wallet_id[0] and to_wallet_id[0]):
        sender_account = guild_collection.find_one({"id": from_wallet_id[1].id})
        reciever_account = guild_collection.find_one({"id": to_wallet_id[1].id})
        if(sender_account is not None):
            if(reciever_account is not None):
                if(sender_account["balance"] > amount):
                    guild_collection.update_one(
                        {"id":  sender_account["id"] },
                        { "$inc":{"balance":-amount} }
                    )
                    guild_collection.update_one(
                        {"id":  reciever_account["id"] },
                        { "$inc":{"balance":amount} }
                    )
                    return (True, "transfer successful")
                else:
                    return (False, "insufficent funds")
            else:
                return (False, "reciever account not found")   
        else:
           return (False, "sender account not found") 
    else:
        return (False, "cannot find wallet")


    pass

def create(guild, wallet_ping, client):
    guild_collection =db[str(guild)]
    get_wallet_result = methods.get_wallet(client, guild, wallet_ping)
    print(get_wallet_result)
    if(get_wallet_result[0]):
        if(get_wallet_result[2] == "person"):
            guild_collection.insert_one({
                "name"   :get_wallet_result[1].name,
                "id"     :get_wallet_result[1].id,
                "type"   :"personal",
                "balance": 0
             })
        else:
            guild_collection.insert_one({
                "name"   :get_wallet_result.name,
                "id"     :get_wallet_result.id,
                "type"   :"role",
                "balance": 0
             })
        return (True, "created")
    else:
        return (False, "doesn't exist")




def get_balance(guild,wallet,client):
    guild_collection =db[str(guild)]
    get_wallet_result = methods.get_wallet(client, guild, wallet)
    print(get_wallet_result)
    if(get_wallet_result[0]):
        found_wallet = guild_collection.find_one({
            "id"     :get_wallet_result[1].id,
        })
        if(found_wallet is None):
            found_wallet = "cannot find wallet"
        return (True, found_wallet)
    else:
        return (False, "doesn't exist")


def print_money(client, guild_id, wallet, amount):
    try:
        amount = int(amount)
    except:
        return (False,"invalid amount" )
    guild_collection =db[str(guild_id)]
    wallet_id = methods.get_wallet(client, guild_id, wallet)
    print(wallet_id)
    if(wallet_id[0]):
        account = guild_collection.find_one({"id": wallet_id[1].id})
        if(account is not None):
                guild_collection.update_one(
                    {"id":  account["id"] },
                    { "$inc":{"balance":amount} }
                )
                return (True, "transfer successful")
        else:
           return (False, "sender account not found") 
    else:
        return (False, "cannot find wallet")

def write_contract(guild,person,contract, trigger ):
    print(trigger, config["triggers"])
    if(trigger not in config["triggers"]):
        return (False, f'invalid trigger types. The supported types are {config["triggers"]}')
    for i in config["illegal_code"]:
        if(i in contract):
            return (False, "contains malicious code")
    guild_collection =db[str(guild_id)]
    contracts = guild_collection.find({
        "type":"contract",
        "author":person.id
    })
    if(contracts > config["max_contracts"]):
        return (False, "you have too many contracts")
    guild_collection.insert_one({
        "type"   :"contract",
        "authour":person.id,
        "trigger": trigger,
        "code": contract
    })
    return (True, "successful")
def trigger_messages(guild, message):
    guild_collection =db[str(guild.id)]

    message_contracts = guild_collection.find({"trigger":"message"})
    print(message_contracts)
    execute_contracts(message_contracts,f'message = {message}' ,guild, )

def execute_contracts(array_of_contracts, context, guild):
    guild_collection =db[str(guild.id)]
    for contract in array_of_contracts:
        try:
            reply = check_output(["python","eval.py",contract.contract, context]).decode('UTF-8')
        except Exception as e:
            guild_collection.deleteOne( { "_id" : contract.__id} );
            reply = "that's an error: {}".format(e)

    

def alter_money(guild, amount,wallet):
    pass
def set_money(guild, amount, wallet):
    pass