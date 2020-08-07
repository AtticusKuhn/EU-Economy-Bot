##this is for the functions that are used many times


import re
import inspect
import types
import json
import jsonpickle
import discord
import threading
import os
from pymongo import MongoClient
import re
import database
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

##finds if a role exists in a server
def is_role(server_roles, role_id):
    server_exists = False
    role_exists = False
    try:
        for server in client.guilds:
            if(server.id == server_id):
                server_exists = True
                found_server = server
                break
    except:
        for server in client["guilds"]:
            if(server.id == server_id):
                server_exists = True
                found_server = server
                break

    if(server_exists):
        for role in found_server.roles:
            if role.id == role_id:
                return (True, role)
        return(False, "role doesn't exist")
    else:
        return (False, "server does not exist")
    


## finds whether a use exists in a server
def is_user(server_id,user_id):
    server_exists = False
    person_exists = False
    try:
        for server in client.guilds:
            if(server.id == server_id):
                server_exists = True
                found_server = server
                break
    except:
        for server in client["guilds"]:
                if(server.id == server_id):
                    server_exists = True
                    found_server = server
                    break
    if(server_exists):
        for person in found_server.members:
            if person.id == user_id:
                return (True, person)
        return(False, "person doesn't exist")
    else:
        return (False, "server does not exist")



def get_wallet(guild, ping_wallet):
    person = discord.utils.find(lambda person: str(ping_wallet) in str(person.name), guild.members)
    if person is not None:
        return (True, person, "person")
    person = discord.utils.find(lambda person: str(re.findall(r'\d{18}',ping_wallet)[0]) == str(re.findall(r'\d{18}',person.mention)[0]), guild.members)
    if person is not None:
            return (True, person, "person")
    role = discord.utils.find(lambda role: str(ping_wallet) in str(role.name), guild.roles)
    if role is not None:
        return (True, role, "role")
    role = discord.utils.find(lambda role: str(re.findall(r'\d{18}',ping_wallet)[0]) == str(re.findall(r'\d{18}',role.mention)[0]), guild.roles)
    if role is not None:
            return (True, role, "role")
    return (False, "not found")


def can_access_wallet(guild, person_id, wallet):
    member = discord.utils.find(lambda m: m.id == person_id, guild.members)
    person_roles= list(map(lambda role: role.id , member.roles))
    server_members = list(map(lambda member:member.id, guild.members))
    server_roles = list(map(lambda role: role.id, guild.roles))
    found_wallet = get_wallet(guild, wallet)
    ##def get_wallet(server_members,server_roles, server_id, ping_wallet):

    ##print("found_wallet is",found_wallet)
    if(not found_wallet[0]):
        ##print(1)
        return False
    if member.guild_permissions.administrator:
        return True
    
    ##print(str(found_wallet[1]),str(person_id) )
    if(str(found_wallet[1].id) == str(person_id)):
        #print(2)
        return True

    #for person in client["members"]:
    #    if(person.id == person_id):
    #            found_person = person
    ##roles = map(lambda role: role.name, found_person.roles)
    if(found_wallet[1].id in person_roles):
        #print(3)
        return True
    guild_collection =db[str(guild.id)]
    account =guild_collection.find_one({"id":found_wallet[1].id})
    print(account)
    if account is not None:
        if "permissions" in account:
            if "access" in account["permissions"]:
                if person_id in account["permissions"]["access"]["true"]:
                    return True
                if person_id in account["permissions"]["access"]["false"]:
                    return False
    for role in member.roles:
        if "permissions" in account:
            if "access" in account["permissions"]:
                if role.id in account["permissions"]["access"]["true"]:
                    return True
    #print(4)
    return False

def isclass(object):
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    #print(isinstance(object, (type, types.ClassType)))
    return isinstance(object, (type, types.ClassType))


def set_interval(func, sec, guild, client):
    def func_wrapper():
        set_interval(func, sec, guild, client)
        func(guild, client)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def whois(message_array, guild):
    print("called as",message_array)
    server_members = set(map(lambda member:member.id,guild.members))

    people = set()
    for index, word in enumerate(message_array):
        word = word.replace("<","")
        word = word.replace("@","")
        word = word.replace("!","")
        word = word.replace(">","")
        word = word.replace("&","")

        if word == "and":
            return people.intersection(whois(message_array[index+1:], guild))
        if word == "or":
            return people.union(whois(message_array[index+1:], guild))
        if word=="not":
            return server_members.difference(whois(message_array[index+1:], guild))
        if word == "everyone":
            people =  server_members
        if word == "online":
            online_people = set()
            for person in guild.members:
                if str(person.status) == "online":
                    online_people.add(person.id)
            
            people =  online_people
            continue
        
        if word == "offline":
            online_people = set()
            for person in guild.members:
                if str(person.status) == "offline":
                    online_people.add(person.id)
            people =  online_people
            continue
        if word == "account":
            guild_collection =db[str(guild.id)]
            online_people = set()
            for person in guild.members:
                has_account = guild_collection.find_one({"id": person.id})
                if has_account:
                    online_people.add(person.id)
            people =  online_people
            continue
        if word == "bot":
            bots = set()
            for person in guild.members:
                if person.bot:
                    bots.add(person.id)
            people =  bots
            continue
        for person in guild.members:
            for perm,value in iter(person.guild_permissions):
                print(perm,value)
                if value and perm == word:
                    people.add(person.id)
        for person in guild.members:
            if person.name == word or str(person.id) == word:
                people.add(person.id)
                #continue
        for role in guild.roles:
            if role.name == word or str(role.id) == word:
                for person in guild.members:
                    if role in person.roles:
                        people.add(person.id)
                        #continue
        
    print(people)
    return people

def valid_item(name):
    pattern = re.compile("^[A-Za-z]{3,10}$")
    return pattern.match(name)



def find_create(wallet_id,guild):
    guild_collection=db[str(guild.id)]
    wallet=guild_collection.find_one({"id":wallet_id})
    if wallet is None:
        res= database.create(guild,f'<@!{wallet_id}>')
        print(res)
        return res[2]
    return wallet


def seconds_to_time(seconds:int):
    seconds = seconds % (24 * 3600) 
    day = seconds // 86400
    seconds %= 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    day =int(day)
    hour = int(hour)
    minutes= int(minutes)
    seconds = int(seconds)
    day = ("1 day " if day==1 else "") if day==0 else f'{day} days '
    hour = ("1 hour " if hour==1 else "") if hour==0 else f'{hour} hours '
    minutes = ("1 minute " if minutes==1 else "") if minutes==0 else  f'{minutes} minutes '
    seconds = ("1 second" if seconds==1 else "" )if seconds==0 else  f'{seconds} seconds'
    return day+hour+minutes+seconds