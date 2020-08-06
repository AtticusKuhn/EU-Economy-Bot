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
import re
from pymongo import MongoClient
#import pprint
import methods
from config import config
from subprocess import check_output
import time
import math
import logging
import random

#import inspect
import asyncio
import discord
from quiz import subject_to_quiz
import database
logging.basicConfig(level=logging.INFO)
#import evaler
#import dnspython 

client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

def send(person_id, guild, from_wallet, to_wallet, amount):
   # #print("send")
    #print("to_wallet is",to_wallet)
    if not methods.can_access_wallet(guild, person_id, from_wallet):
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
    guild_collection =db[str(guild.id)]
    from_wallet_id = methods.get_wallet(guild, from_wallet)
    to_wallet_id =methods.get_wallet(guild, to_wallet)
    #print(to_wallet_id,from_wallet_id)
    if(from_wallet_id[0] and to_wallet_id[0]):
        sender_account = guild_collection.find_one({"id": from_wallet_id[1].id})
        reciever_account = guild_collection.find_one({"id": to_wallet_id[1].id})
        if(sender_account is None):
            c_result = create(guild, from_wallet)
            if not c_result[0]:
                return (False,c_result[1] )
            sender_account=c_result[2]  
        if(reciever_account is None):
            c_result = create(guild, to_wallet)
            if not c_result[0]:
                return (False,c_result[1] )
            reciever_account=c_result[2]

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
            log_money(guild,f'<@{person_id}> sent {amount} from {from_wallet} to {to_wallet}')
            return (True, f'transfer successful. you send {amount}, making your balance '+ str(sender_account[f'balance{currency}'])+f' {currency}')
                
        else:
           return (False, f'insuffiecent funds for transfer.') 
    else:
        return (False, "cannot find wallet")


    pass

def create(guild, wallet_ping):
    guild_collection =db[str(guild.id)]
    get_wallet_result = methods.get_wallet( guild, wallet_ping)
    
    #print(get_wallet_result)
    server_config =  guild_collection.find_one({
            "type":"server",
            "id"  : guild.id
    })
    if server_config is not None:
        default_balance =server_config["default_balance"]
    else:
        guild_collection.insert_one({
            "type":"server",
            "id":guild.id,
            "default_balance": config["default_balance"]
        })
        default_balance = config["default_balance"]
    if(get_wallet_result[0]):
        if guild_collection.find_one({ "id":get_wallet_result[1].id}):
            return (False, "account already exists")
        name = ""
        for person in guild.members:
            if(person.id == get_wallet_result[1].id):
                found_person = person
       # for guild_obj in client.guilds:
       #     if guild_obj.id == guild:
       #         found_guild =guild_obj 
        for role in guild.roles:
            if(role.id == get_wallet_result[1].id):
                found_role = role
        if(get_wallet_result[2] == "person"):
            return_wallet = guild_collection.insert_one({
                "name"   :found_person.name,
                "id"     :found_person.id,
                "type"   :"personal",
                "balance": int(default_balance)
             })
            return_wallet = guild_collection.find_one({"id":return_wallet.inserted_id})
        else:
            return_wallet = guild_collection.insert_one({
                "name"   :found_role.name,
                "id"     :found_role.id,
                "type"   :"role",
                "balance": int(default_balance)
             })
            return_wallet = guild_collection.find_one({"_id":return_wallet.inserted_id})
        return (True, "created",return_wallet)
    else:
        return (False, "doesn't exist")




def get_balance(person, guild,wallet):
    guild_collection =db[str(guild.id)]
    ##(server_members,server_roles,  guild_id, from_wallet)
    get_wallet_result = methods.get_wallet(guild, wallet)
    #print(get_wallet_result)
       
    if(get_wallet_result[0]):
        found_wallet = guild_collection.find_one({"id":get_wallet_result[1].id})
        if(found_wallet is None):
            found_wallet = create(guild, wallet)[2]
        if "permissions" in found_wallet:
            if "view" in found_wallet["permissions"]:
                print(1)
                if person.id in found_wallet["permissions"]["view"]["false"]:
                    print(2)
                    return (False, "you do not have permission to see this wallet")
        return (True, found_wallet)
    else:
        return (False, "doesn't exist")


def print_money(person,guild, wallet, amount):
    currency=""
    if "-" in amount:
        currency=f'-{amount.split("-")[1]}'
        amount =amount.split("-")[0]

        if not methods.valid_item(currency[1:]):
            return (False, "invalid item name")
    try:
        amount = int(amount)
    except:
        return (False,"invalid amount" )
    
    guild_collection =db[str(guild.id)]
    wallet_id = methods.get_wallet(guild, wallet)
    if not wallet_id[0]:
        return (False,"invalid wallet name")
    can_print = False
    if person.guild_permissions.administrator:
        can_print=True
    account_of_printing =guild_collection.find_one({"id":wallet_id[1].id})
    if account_of_printing is None:
        c_result = create(guild, wallet)
        if not c_result[0]:
            return (False,c_result[1] )
        account_of_printing=c_result[2]
        #return (False,"can't find doesn't exist")
    if "permissions" in account_of_printing:
        if "print" in account_of_printing["permissions"]:
            if person.id in account_of_printing["permissions"]["print"]["true"]:
                can_print = True
            for role in person.roles:
                if role.id in account_of_printing["permissions"]["print"]["true"]:
                    can_print = True
        if currency != "":
            if f'print{currency}' in account_of_printing["permissions"]:
                if person.id in account_of_printing["permissions"][f'print{currency}']["true"]:
                    can_print = True
                for role in person.roles:
                    if role.id in account_of_printing["permissions"][f'print{currency}']["true"]:
                        can_print = True
    if "printer" in person.roles:
        can_print=True
    if not can_print:
        return (False, "you do not have permission to print")
    guild_collection.update_one(
        {"id":  account_of_printing["id"] },
        { "$inc":{f'balance{currency}':amount} }
    )
    return (True, "transfer successful")
    ##get_wallet(server_members,server_roles, server_id, ping_wallet)
    #print(wallet_id)
    #if(wallet_id[0]):
        #account = guild_collection.find_one({"id": wallet_id[1].id})
        #if(account is not None):
        
        #else:
        #   return (False, "sender account not found") 
    #else:
     #   return (False, "cannot find wallet")

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
        contract["code"] = contract["code"].replace("send(",f'send({contract["args"][3]}, message.guild,')
        safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', "message", "context","locals"] 
        safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) 
        safe_dict["send"] = send
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
                #print(inspect.iscoroutinefunction(contract["code"]))
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
    if setting_name in ["default_balance","quiz-payoff", "quiz-cooldown","work-payoff","work-cooldown"]:
        if not option.isdigit():
            return (False, "must be a number")
        option=int(option)
    
    if setting_name not in config["config_options"]:
        return (False, f'cannot find that setting; Currently supported settings are ${", ".join(config["config_options"])} ')
    if setting_name == "log-channel":
        match = re.match(r'<#\d{18}>', option)
        print(match)
        if match is None:
            return (False, "invalid channel")
        option = re.findall(r'\d{18}', option)[0]
        print(option)
    guild_collection.update_one({
    '_id': server_config['_id']
    },{
        '$set': {
        setting_name :option
        }
    })
    return (True, "success")


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
    to_wallet = methods.get_wallet(guild, wallet)
    if(not to_wallet[0]):
        return to_wallet
    if 'currency' in locals():
        guild_collection.update_one(
            {"id":  to_wallet[1].id },
            { "$set":{f'balance-{currency}':int(amount)} }
        )
        return (True, f'balance was set to {amount}')
    guild_collection.update_one(
        {"id":  to_wallet[1].id },
        { "$set":{"balance":int(amount)} }
    )
    return (True, f'balance was set to {amount}')

def set_settings(guild, person,target, wallet, setting_name, value):
    if not setting_name in config["wallet_settings"] and not setting_name.startswith("print-"):
        return (False, "invalid setting name")
    value = (value.lower() == "true")
    found_wallet =methods.get_wallet(guild, wallet)
    found_target = methods.get_wallet(guild, target)
    if not found_wallet[0]:
        return (False, "wallet does not exist")
    if not found_target[0]:
        return (False, "target does not exist")
    guild_collection =db[str(guild.id)]
    account =guild_collection.find_one({"id":found_wallet[1].id})
    if not account:
        return (False,"wallet does not have an accound")
    can_access = False
    if person.guild_permissions.administrator:
        can_access = True
    if not can_access:
        return (False, "you cannot edit the settings of this wallet")
    temp = account
    print(temp, setting_name)
    if not "permissions" in temp:
        temp["permissions"] = {
        }
    if temp["permissions"] is None:
        temp["permissions"] = {
        }
    if not setting_name in temp["permissions"]:
        temp["permissions"][setting_name] ={
            "true":[],
            "false":[]
        }
    if not "true" in temp["permissions"][setting_name]:
        temp["permissions"][setting_name] ={
            "true":[],
            "false":[]
        }
    if value:
        if found_target[1].id in temp["permissions"][setting_name]["true"]:
            return (False, "setting already true")
        temp["permissions"][setting_name]["true"].append(found_target[1].id)
        try:
            temp["permissions"][setting_name]["false"].remove(found_target[1].id)
        except:
            pass

    else:
        if found_target[1].id in temp["permissions"][setting_name]["false"]:
            return (False, "setting already false")
        temp["permissions"][setting_name]["false"].append(found_target[1].id)
        try:
            temp["permissions"][setting_name]["true"].remove(found_target[1].id)
        except:
            pass
    guild_collection.update_one(
        {"id":found_wallet[1].id},
        { "$set":{"permissions":temp["permissions"]}}
    )
    return (True, "settings successfully changed")

def  insert_trade(message, person, guild,wallet, offer,cost, options):
    if wallet !="admins":
        found_wallet=methods.get_wallet(guild,wallet)
        if not found_wallet[0]:
            return (False, "bad wallet")
        if not methods.can_access_wallet(guild, person.id, wallet):
            return (False,"bad wallet 2")

    offer_currency=""
    offer_amount = offer
    if "-" in offer:
        offer_currency=f'-{offer.split("-")[1]}'
        offer_amount =offer.split("-")[0]
        if not methods.valid_item(offer_currency[1:]):
            return (False, "invalid item name")
    cost_currency=""
    cost_amount = cost
    if "-" in cost:
        cost_currency=f'-{cost.split("-")[1]}'
        cost_amount =cost.split("-")[0]
        if not methods.valid_item(cost_currency[1:]):
            return (False, "invalid item name")
    if re.match(r'<@&?\d{18}>', offer) is not None:
        offer_currency = offer
        offer_amount="1"
    #offer_amount = offer.split("-")[0]
    #offer_currency = offer.split("-")[1]
    #cost_amount = cost.split("-")[0]
    #cost_currency = cost.split("-")[1]
    print(offer_amount,cost_amount)
    if not offer_amount.isdigit() or not cost_amount.isdigit():
        return (False, "invalid amount")
    offer_amount=int(offer_amount)
    cost_amount=int(cost_amount)
    for index, option in enumerate(options):
        if "use" in option:
            if not option.split("use")[0].isdigit():
                return (False, "invalid uses")
            uses = option.split("use")[0]
        if "time" in option:
            if not option.split("time")[0].isdigit():
                return (False, "invalid time")
            offer_time = int(option.split("time")[0]) +time.time()
        if option=="whois":
            people_restrictions = options[index:]
    guild_collection =db[str(guild.id)]
    offer_schema = {
        "type":"trade",
        "person":person.id,
        "message_id":message.id,
        "offer_currency":offer_currency,
        "offer_amount":int(offer_amount),
        "cost_currency":cost_currency,
        "cost_amount":int(cost_amount)
    }
    if "found_wallet" in locals():
        offer_schema["wallet"] = found_wallet[1].id
    if "uses" in locals():
        offer_schema["uses"]=int(uses)
    if "offer_time" in locals():
        offer_schema["offer_time"]=int(offer_time)
    if "people_restrictions" in locals():
        offer_schema["people_restrictions"] = people_restrictions
    guild_collection.insert_one(offer_schema)
    return (True, f'succesful. In order to accept this trade, type "$accept {message.id} (ping wallet)", or you may react to the original message with ✅, in which case the money will be deducted from your personal account.')


def fulfill_trade(message,wallet, person, guild):
    found_wallet = methods.get_wallet(guild, wallet)
    if not found_wallet[0]:
        return (False,"cant find wallet")
    if not methods.can_access_wallet(guild, person.id, wallet):
        return (False, "cannot access wallet")
    try:
       message=int(message)
    except:
        return (False,"invalid number")
    guild_collection =db[str(guild.id)]
    found_offer=guild_collection.find_one({
        "type":"trade",
        "message_id"  :message
    })
    if found_offer is None:
        return (False, "can't find offer")
    if "uses" in found_offer:
        if found_offer["uses"] <=0:
            guild_collection.delete_one({"message_id":found_offer["message_id"]})
            return (False,"offer has been used up")
    if "offer_time" in found_offer:
        if time.time() > found_offer["offer_time"]:
            guild_collection.delete_one({"message_id":found_offer["message_id"]})
            return (False,"offer has run out of time")
    if "people_restrictions" in found_offer:
        if person.id not in methods.whois(found_offer["people_restrictions"],guild):
            return (False, "you cannot accept this offer because a restriction has bee")
    receiver = guild_collection.find_one({"id":found_wallet[1].id})
    if receiver is None:
        c_result = create(guild, wallet)
        if not c_result[0]:
            return (False,c_result[1] )
        receiver=c_result[2]
    if f'balance{found_offer["cost_currency"]}' not in receiver:
        return (False, "you have no money")
    if receiver[f'balance{found_offer["cost_currency"]}'] < found_offer["cost_amount"]:
        return (False,"you don't have enough money")
    sender =  guild_collection.find_one({"id":found_offer["person"]})
    if "wallet" in found_offer:
        if f'balance{found_offer["offer_currency"]}' not in sender:
            guild_collection.delete_one({"message_id":found_offer["message_id"]})
            return (False, "offer deleted, person does not have enough for trade")
        if sender[f'balance{found_offer["offer_currency"]}'] < found_offer["offer_amount"]:
            guild_collection.delete_one({"message_id":found_offer["message_id"]})
            return (False, "offer deleted, person does not have enough for trade")
    guild_collection.update_one(
        {"id":  receiver["id"] },
        { "$inc":{f'balance{found_offer["offer_currency"]}':-int(found_offer["offer_amount"])} }
    )
    guild_collection.update_one(
        {"id":  receiver["id"] },
        { "$inc":{f'balance{found_offer["cost_currency"]}':int(found_offer["cost_amount"])} }
    )
    if" wallet" in  found_offer:
        guild_collection.update_one(
            {"id":  sender["id"] },
            { "$inc":{f'balance{found_offer["offer_currency"]}':int(found_offer["offer_amount"])} }
        )
        guild_collection.update_one(
            {"id":  sender["id"] },
            { "$inc":{f'balance{found_offer["cost_currency"]}':-int(found_offer["cost_amount"])} }
        )
    if re.match(r'<@&?\d{18}>', found_offer["offer_currency"]) is not None:
        try:
            loop = asyncio.get_event_loop()
            id_role= re.findall(r'\d{18}', found_offer["offer_currency"])[0]
            print(id_role)
            id_role=int(id_role)
            role = discord.utils.get(guild.roles, id=id_role)
            print(role)
            loop.create_task(person.add_roles(role))
        except:
            return (False,"bad permissions")
    if "uses" in found_offer:
        guild_collection.update_one(
            {"message_id":  found_offer["message_id"] },
            { "$inc":{"uses":-1} }
        )
    return (True,"success")

def log_money(guild, message):
    print("log_money called")
    guild_collection = db[str(guild.id)]
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    if server_config is None:
        return
    print("config is not none")
    if "log-channel" not in server_config:
        return
    print("log-channel exists and it is", server_config["log-channel"])
    channel = discord.utils.find(lambda m: str(m.id) == str(server_config["log-channel"]), guild.channels)
    if channel is None:
        return
    print("found channel")
    #asyncio.run(channel.send(f'log: {message}'))
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(channel.send(f'log: {message}'))

def get_question(person, guild):
    guild_collection=db[str(guild.id)]
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    if server_config is None:
        return (False, "server config is not set up. Ask your admin to set up the config")
    quiz_cooldown = config["quiz-cooldown"]
    if "quiz-cooldown" in server_config:
        quiz_cooldown = server_config["quiz-cooldown"]
    person_wallet = guild_collection.find_one({"id":person.id})
    if person_wallet is not None:
        if "quiz-cooldown" in person_wallet:
            if time.time() - person_wallet["quiz-cooldown"] <quiz_cooldown:
                return (False,"wait for the cooldown to end")
    guild_collection.update_one(
        {"id":person.id},
        {"$set":{"quiz-cooldown":time.time()}}
    )
    #try:
    question = subject_to_quiz(server_config["quiz-subject"])
    print(question,"question")

    #except:
    #    return (False, "error")
    guild_collection.insert_one({
        "type":"quiz",
        "person":person.id,
        "question":question,
        "time":time.time()
    })
    return (True, question["question"])
def answer_question(person, answer, guild):
    guild_collection=db[str(guild.id)]
    question = guild_collection.find_one({"type":"quiz","person":person.id})
    if question is None:
        return None
    guild_collection.delete_one({"type":"quiz","person":person.id})
    if time.time() - question["time"] >10000:
        return (False, "you ran out of time sorry")
    if question["question"] is not None:
        if "answer" in  question["question"]:
            if question["question"]["answer"] != answer and answer not in question["question"]["similar_words"]:
                return (False,f'inrrect answer, correct answer is {question["question"]["answer"]}')
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    if server_config is not None and "quiz-payoff" in server_config:
        guild_collection.update_one(
            {"id":  person.id },
            { "$inc":{f'balance':server_config["quiz-payoff"]} }
        )
        return (True, f'your balance has been increased by {server_config["quiz-payoff"]}')

    guild_collection.update_one(
        {"id":  person.id },
        { "$inc":{f'balance':1} }
    )
    if answer in question["question"]["similar_words"]:
        return (True, f'the correct answer was {question["question"]["answer"]}, but that was close enough to be correct.')
    return (True, "your balance has been increased by one")

def work(person,guild):
    wallet = methods.find_create(person.id,guild)
    cooldown = config["work-cooldown"]
    guild_collection=db[str(guild.id)]

    server_config =  guild_collection.find_one({
        "type":"server","id"  : guild.id
    })
    if server_config is not None:
        if "work-cooldown" in server_config:
            cooldown = server_config["work-cooldown" ]
    if "cooldown-work" in wallet:
        print(time.time(), wallet["cooldown-work"],time.time() - wallet["cooldown-work"], cooldown)
        if time.time() - wallet["cooldown-work"] < cooldown:
            return (False,"wait to work")
    payout=config["work-payoff"]
    if server_config is not None:
        if "work-payoff" in server_config:
            payout = server_config["work-payoff" ]
    guild_collection.update_one(
        {"id":  person.id },
        { "$inc":{f'balance':payout} }
    )
    guild_collection.update_one(
        {"id":  person.id },
        { "$set":{f'cooldown-work':time.time()} }
    )
    lines = open('jobs.txt').read().splitlines()
    job =random.choice(lines)
    return (True,f'You worked as {job} and earned {payout}')
    