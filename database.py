##this files is where the database stores info about money





#general form of a wallet will be
#{
#   "name"   :"eulerthedestroyer",
#   "id"     :464954455029317633,
#   "type"   :"personal",
#   "balance": 5
#}
import PyMongo
from pymongo import MongoClient
import pprint
import methods

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database


def send(guild, from_wallet, to_wallet, amount):
    guild_collection =db[guild.id]
    from_wallet_id = methods.get_wallet(guild, from_wallet)
    to_wallet_id =methods.get_wallet(guild, to_wallet)
    if(from_wallet_id[0] and to_wallet_id[0])
        sender_account = guild_collection.find_one(posts.find_one({"id": from_wallet_id[1]}))
        reciever_account = guild_collection.find_one(posts.find_one({"id": to_wallet_id[1]}))
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

def create(guild, wallet_ping):
    guild_collection =db[guild.id]
    get_wallet_result = methods.get_wallet(guild wallet_ping)
    if(get_wallet_result[0]):
        if(get_wallet_result[2] == "person"):
            guild_collection.insert_one({
                "name"   :get_wallet_result.username,
                "id"     :get_wallet_result.id,
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
    else:
        return (False, "doesn't exist")




def get_balance(guild,wallet):
    pass
def alter_money(guild, amount,wallet):
    pass
def set_money(guild, amount, wallet):
    pass