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
from subprocess import check_output
import time
import math
#import evaler
#import dnspython 

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

def simple_send(person_id,guild, from_wallet, to_wallet, amount):
    found = (False, "e")
    for person in guild.members:
        if person.id == person_id:
            found = (True,person)
            break
    if not found[0]:
        return (False, "not found")
    person_roles= list(map(lambda role: role.id , found[1].roles))
    server_members = list(map(lambda member:member.id, guild.members))
    server_roles = list(map(lambda role: role.id, guild.roles))
    return send(person_roles, server_members, server_roles, person_id, guild.id, from_wallet, to_wallet, amount)
 
def send(person_roles, server_members, server_roles, person_id, guild_id, from_wallet, to_wallet, amount):
   # #print("send")
    #print("to_wallet is",to_wallet)
    if not methods.can_access_wallet(server_roles, server_members, person_roles, guild_id, person_id, from_wallet):
        return (False, "cannot access wallet")
    currency=""
    if "-" in amount:
        currency=f'-{amount.split("-")[1]}'
        amount =amount.split("-")[0]
    percent = False
    if "%" in amount:
        percent = True
        amount =amount.split("%")[0]
    try:
        amount = int(amount)
    except:
        return (False,"invalid amount" )
    guild_collection =db[str(guild_id)]
    from_wallet_id = methods.get_wallet(server_members,server_roles,  guild_id, from_wallet)
    to_wallet_id =methods.get_wallet(server_members,server_roles,  guild_id, to_wallet)
    #print(to_wallet_id,from_wallet_id)
    if(from_wallet_id[0] and to_wallet_id[0]):
        sender_account = guild_collection.find_one({"id": from_wallet_id[1]})
        reciever_account = guild_collection.find_one({"id": to_wallet_id[1]})
        if(sender_account is not None):
            if(reciever_account is not None):
                if f'balance{currency}' not in sender_account:
                    return (False, "you do not have this currency")
                if percent:
                    amount = math.floor(sender_account[f'balance{currency}']*(amount/100))
                if(sender_account[f'balance{currency}'] > amount):
                    guild_collection.update_one(
                        {"id":  sender_account["id"] },
                        { "$inc":{f'balance{currency}':-amount} }
                    )
                    guild_collection.update_one(
                        {"id":  reciever_account["id"] },
                        { "$inc":{f'balance{currency}':amount} }
                    )
                    return (True, f'transfer successful. you send {amount}, making your balance '+ str(sender_account[f'balance{currency}'])+f' {currency}')
                else:
                    return (False, "insufficent funds")
            else:
                return (False, "reciever account not found")   
        else:
           return (False, "sender account not found") 
    else:
        return (False, "cannot find wallet")


    pass

def create(guild, wallet_ping, server_members,server_roles, client):
    guild_collection =db[str(guild)]
    get_wallet_result = methods.get_wallet(server_members,server_roles, guild, wallet_ping)
    #print(get_wallet_result)
    server_config =  guild_collection.find_one({
            "type":"server",
            "id"  : guild
    })
    if server_config is not None:
        default_balance =server_config["default_balance"]
    else:
        guild_collection.insert_one({
            "type":"server",
            "id":guild,
            "default_balance": config["default_balance"]
        })
        default_balance = config["default_balance"]
    if(get_wallet_result[0]):
        name = ""
        for person in client.users:
            if(person.id == get_wallet_result[1]):
                found_person = person
        for guild_obj in client.guilds:
            if guild_obj.id == guild:
                found_guild =guild_obj 
        for role in found_guild.roles:
            if(role.id == get_wallet_result[1]):
                found_role = role
        if(get_wallet_result[2] == "person"):
            guild_collection.insert_one({
                "name"   :found_person.name,
                "id"     :found_person.id,
                "type"   :"personal",
                "balance": default_balance
             })
        else:
            guild_collection.insert_one({
                "name"   :found_role.name,
                "id"     :found_role.id,
                "type"   :"role",
                "balance": default_balance
             })
        return (True, "created")
    else:
        return (False, "doesn't exist")




def get_balance(guild,wallet,server_members, server_roles):
    guild_collection =db[str(guild)]
    ##(server_members,server_roles,  guild_id, from_wallet)
    get_wallet_result = methods.get_wallet(server_members,server_roles, guild, wallet)
    #print(get_wallet_result)
    if(get_wallet_result[0]):
        found_wallet = guild_collection.find_one({
            "id"     :get_wallet_result[1],
        })
        if(found_wallet is None):
            return (False, "cannot find wallet")
        return (True, found_wallet)
    else:
        return (False, "doesn't exist")


def print_money(server_members,server_roles, discord_client, guild_id, wallet, amount):
    currency=""
    if "-" in amount:
        currency=f'-{amount.split("-")[1]}'
        amount =amount.split("-")[0]
    try:
        amount = int(amount)
    except:
        return (False,"invalid amount" )
    
    guild_collection =db[str(guild_id)]
    ##get_wallet(server_members,server_roles, server_id, ping_wallet)
    wallet_id = methods.get_wallet(server_members,server_roles, guild_id, wallet)
    #print(wallet_id)
    if(wallet_id[0]):
        account = guild_collection.find_one({"id": wallet_id[1]})
        if(account is not None):
                guild_collection.update_one(
                    {"id":  account["id"] },
                    { "$inc":{f'balance{currency}':amount} }
                )
                return (True, "transfer successful")
        else:
           return (False, "sender account not found") 
    else:
        return (False, "cannot find wallet")

def write_contract(guild,person,contract, trigger, discord_client, *arg ):
    #print(trigger, config["triggers"])
    if(trigger not in config["triggers"]):
        return (False, f'invalid trigger types. The supported types are {config["triggers"]}')
    for i in config["illegal_code"]:
        if(i in contract):
            return (False, "contains malicious code")
    if "set_money" in contract and not person.guild_permissions.administrator:
        return (False, "only admins can use set_money")
    guild_collection =db[str(guild.id)]
    contracts = guild_collection.find({
        "type":"contract",
        "author":person.id
    })
    if(len(list(contracts)) > config["max_contracts"]):
        return (False, "you have too many contracts")
    guild_collection.insert_one({
        "type"   :"contract",
        "author":person.id,
        "trigger": trigger,
        "code": contract,
        "args":arg
    })
    return (True, "successful")
def trigger_messages(guild, message,  person_roles,server_members,server_roles,person_id):
    #print("trigger_messages")
    guild_collection =db[str(guild.id)]

    message_contracts = guild_collection.find({"trigger":"message"})
    #print(message_contracts)
   
    #props = [attr for attr in dir(message) if not callable(getattr(message, attr)) and not attr.startswith("_")]
   # dict_message =str({
    #    "message":message.id,
   #     "type":"message",
    #    "channel":message.channel.id,
     #   "guild":message.guild.id
   # })
    dict_message = message
    ##print(dict_message)
    #methods.class_to_dict(message)
    #dict_client = methods.class_to_dict(discord_client)
    ##print("dict_client is",dict_client, "and discord_client is",discord_client)
    return execute_contracts(message_contracts,dict_message ,guild,person_roles,server_members,server_roles,person_id )
def trigger_time(guild,client):
    record_balances(guild,client)

    guild_collection =db[str(guild.id)]
    message_contracts = guild_collection.find({"trigger":"day"})
    guild_dict ="idk this is a placeholder"#methods.class_to_dict(guild)

    res =  execute_contracts(message_contracts ,guild_dict, guild,  "'placeholder'","'placeholder'","'placeholder'","'placeholder'" )
    for user in guild.members:
        if len(res) == 1:
            if user.id == res[0][2]:
                print(res)
    return res
def execute_contracts(array_of_contracts, context, guild, person_roles,server_members,server_roles,person_id):
    #print("execute_contracts")
    guild_collection =db[str(guild.id)]
    result = []
    for contract in array_of_contracts:
        #try:

        ##print(["python","eval.py",contract["code"], context])
        person_roles = str(person_roles)
        server_members = str(server_members)
        server_roles = str(server_roles)
        person_id = str(person_id)
        #print(contract["args"],"is contract['args']")
        contract["code"] = contract["code"].replace("send(",f'send({contract["args"][3]},')
        safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', "message", "context","locals"] 
        safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) 
        safe_dict["send"] = simple_send
        safe_dict["whois"] = methods.whois
        safe_dict["set_money"] = set_money
        
        if contract["trigger"] == "day":
            #contract["code"] = contract["code"].replace("send(",f'send({contract["args"][0]}, {contract["args"][1]}, {contract["args"][2]}, {contract["args"][3]}, {guild.id},')
            try:
                #print("message is", message)
                #contract["code"] = contract["code"].replace("send(",f'send({person_roles}, {server_members}, {server_roles}, {person_id}, {guild.id},')
                
                safe_dict["guild"]=guild
                safe_dict['time'] = time

                exec(contract["code"],{"__builtins__":None},safe_dict)
                reply = str(safe_dict["output"])
            except Exception as e:
                reply = f'error:{e}'
            #reply = check_output(["python","eval.py",contract["code"], context,  str(contract["args"][0]),str(contract["args"][1]),str(contract["args"][2]),str(contract["args"][3])]).decode('UTF-8')
        elif contract["trigger"] == "message":
            try:
                message = context
                #print("message is", message)
                #contract["code"] = contract["code"].replace("send(",f'send({person_roles}, {server_members}, {server_roles}, {person_id}, {guild.id},')
                #safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', "message", "context","locals"] 
                #safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) 
                safe_dict['message'] = message

                exec(contract["code"],{"__builtins__":None},safe_dict)
                #print(safe_dict)
                if "output" in safe_dict:
                    reply = str(safe_dict["output"])
                else:
                    reply = None
                    continue
            except Exception as e:
                reply = f'error:{e}'
               

            #reply = check_output(["python","eval.py",contract["code"], context,  person_roles,server_members,server_roles,person_id]).decode('UTF-8')
        if( len(reply) > config["max_length"]):
            guild_collection.delete_one( { "_id" : contract["_id"]} )
            result.append((False, "message too long", contract["author"]))
        elif("error" in reply or "annul" in reply):
            guild_collection.delete_one( { "_id" : contract["_id"]} )
            result.append((False, reply, contract["author"]))
        else:
            result.append((True, reply, contract["author"]))

        #print(result)
       # except Exception as e:
        #    #print(e)
         #   guild_collection.delete_one( { "_id" : contract["_id"]} );
          #  reply = "that's an error: {}".format(e)
           # result.append((False, reply, contract["author"]))
    #print(result,"result")
    return result

def all_db(guild):
    result = []
    guild_collection =db[str(guild.id)]
    cursor = guild_collection.find() 

    return list(cursor)

def clear_contracts(guild,person_id):
    guild_collection =db[str(guild.id)]
    guild_collection.delete_many({
        "type":'contract',
        "author":person_id
    })
def set_config(guild, setting_name, option):
    guild_collection =db[str(guild.id)]
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    if server_config is None:
        guild_collection.insert_one({
            "type":"server",
            "id":guild.id,
            "default_balance": config["default_balance"]
        })
#print(setting_name)
    if setting_name not in config["config_options"]:
        return "can't find that setting"
    guild_collection.update_one({
    '_id': server_config['_id']
    },{
        '$set': {
        setting_name :option
        }
    })
    return server_config


def  record_balances(guild,client):
    guild_collection =db[str(guild.id)]
    role_wallets = guild_collection.find({"type":"role"})
    person_wallets = guild_collection.find({"type":"personal"})

    for wallet in person_wallets:
        temp = wallet
       # if "record" not in temp:
           # temp["record"] = {}
        #print(f'inital of {wallet["name"]} is {wallet["record"]}')
        try:
            temp["record"][str(time.time())] = wallet["balance"]
        except:
            temp["record"] = {}
            temp["record"][str(time.time())] = wallet["balance"]

        guild_collection.update_one(
            {"id":  wallet["id"] },
            { "$set":{"record":temp["record"]} }
        )
        print(f'recording the wallet of {wallet["name"]}, it is {wallet["record"]}')
    for wallet in role_wallets:
        temp = wallet
        if "record" not in temp:
            temp["record"] = {}
        temp["record"][str(time.time())] = wallet["balance"]
        guild_collection.update_one(
            {"id":  wallet["id"] },
            { "$set":{"record":temp["record"]} }
        )
    print("balance recorded")
def wallet_by_id(guild,person_id):
    guild_collection =db[str(guild.id)]
    print( guild_collection.find_one({"id":int(person_id)}))
    return guild_collection.find_one({"id":int(person_id)})




def set_money(guild, amount,wallet):
    server_members = list(map(lambda member:member.id, guild.members))
    server_roles = list(map(lambda role: role.id, guild.roles))
    if("-" in amount):
        amount_array = amount.split("-")
        print(amount.split("-"))
        amount = amount_array[0]
        currency = amount_array[1]
    if 'currency' in locals():
        if(not methods.valid_item(currency)):
            return (False, "invaid item name")
    if(not amount.isdigit()):
        return (False, "incorrect ammount")
    guild_collection =db[str(guild.id)]
    to_wallet = methods.get_wallet(server_members,server_roles,  guild.id, wallet)
    if(not to_wallet[0]):
        return to_wallet
    if 'currency' in locals():
        guild_collection.update_one(
            {"id":  to_wallet[1] },
            { "$set":{f'balance-{currency}':int(amount)} }
        )
        return (True, f'balance was set to {amount}')
    guild_collection.update_one(
        {"id":  to_wallet[1] },
        { "$set":{"balance":int(amount)} }
    )
    return (True, f'balance was set to {amount}')

def alter_money(guild, amount, wallet, person):
    guild_collection =db[str(guild.id)]
