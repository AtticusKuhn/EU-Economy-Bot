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



def get_wallet(server_members,server_roles, server_id, ping_wallet):
    ##print("ping_wallet is", ping_wallet)
    server_exists = False
    wallet_exists = False
    found_server =""
    ###print(ping_wallet,"ping_waller")
   # try:
    #    for server in client.guilds:
     #       if(server.id == server_id):
#                server_exists = True
#                found_server = server
#                break
#    except:
#        for server in client["guilds"]:
#            if(server.id == server_id):
#                server_exists = True
#                found_server = server
#                break
#    if(server_exists):
    digit = re.search(r"\d", ping_wallet)
    if digit is not None:
        id_of_wallet = ping_wallet[digit.start():-1]
        ##print(id_of_wallet, "is id_of_wallet")
        ##print("server_members is",server_members)
        for person in server_members:
            ##print("person is",str(person), "wallet id is ", str(id_of_wallet))
            if str(person) == str(id_of_wallet):
                return (True, person, "person")
        for role in server_roles:
            if str(role) == str(id_of_wallet):
                return (True, role, "role")
        return (False, "not found")
    else:
        return (False, "invalid format")
    #else:
     #   return (False, "server does not exist")


def can_access_wallet(server_roles, server_members, person_roles, server_id, person_id, wallet):
    found_wallet = get_wallet(server_members, server_roles, server_id, wallet)
    ##print("found_wallet is",found_wallet)
    if(not found_wallet[0]):
        ##print(1)
        return False
    
    ##print(str(found_wallet[1]),str(person_id) )
    if(str(found_wallet[1]) == str(person_id)):
        #print(2)
        return True
    try:
        for person in client.members:
            if(person.id == person_id):
                found_person = person
    except:
        for person in client["members"]:
            if(person.id == person_id):
                found_person = person
    ##roles = map(lambda role: role.name, found_person.roles)
    if(found_wallet[1].name in person_roles):
        #print(3)
        return True
    #print(4)
    return False

    
#def class_to_dict(class_instance):
#    props = {}
#    for attr in dir(class_instance):
#        called =True
#        try:
#            if not callable(getattr(class_instance, attr)):
#                called = False
#        except:
#            pass
#        if not called:
#            if not attr.startswith("_") and getattr(class_instance, attr) is not None:
#                ##print(callable(getattr(class_instance, attr)))
#                ##print("the attr is",attr, not attr.startswith("_"))
#                ##print("getattr is",  getattr(class_instance, attr))
#                ##print(type(getattr(class_instance, attr)))
#                if  str(getattr(class_instance, attr)).startswith("<"): #or getattr(class_instance, attr).startswith("<") : 
#                    if type(getattr(class_instance, attr)) is not list:
#                        props[attr] = class_to_dict(getattr(class_instance, attr))
#                        ##print("adding to 1")
#                else: #not callable(getattr(class_instance, attr))# and not attr.startswith("_"):
#                    props[attr] = getattr(class_instance, attr)
#                    ##print("attr is",getattr(class_instance, attr))              
#    
#    #for key in props:
#     ##   if type(props[key]) is not str or type(props[key]) is not bool or type(props[key]) is not dict or type(props[key]) is not list or type(props[key]) is not int:
#       ##     props[key] = ""
#    props = str(props)
#    props.replace("<",'"')
#    props.replace("<",'"')
#    props.replace(">",'"')
#    props.replace(">",'"')
#    ##print("final result is", props)
#    return props
def isclass(object):
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    #print(isinstance(object, (type, types.ClassType)))
    return isinstance(object, (type, types.ClassType))


def class_to_dict(class_instance,depth = 0):
    props = {}
    for attr in dir(class_instance):
        try:
            if(attr.startswith("_")):
                continue##print(attr, str(getattr(class_instance, attr))[0] )
        except:
            pass
        if(depth>2):
            props[attr] = ''
            continue
       

        try:
           # #print(type(getattr(class_instance, attr)) is discord.member.Member)
            will_delete = True
        
            #if (str(getattr(class_instance, attr)).startswith("<") and not attr.startswith("_") and not callable(getattr(class_instance, attr))): # or attr == "author" or attr == "channel" or attr=="Guild" or attr =="Member" )and not attr.startswith("_") and not callable(getattr(class_instance, attr)):
            #    depth+=1
           #     props[attr] = class_to_dict(getattr(class_instance, attr), depth)
            #    will_delete = False
            if not callable(getattr(class_instance, attr)) and not attr.startswith("_"):
                props[attr] = getattr(class_instance, attr)
                will_delete = False
                
            if type(getattr(class_instance, attr)) is discord.member.Member:
                props[attr] =  class_to_dict(getattr(class_instance, attr), depth)
                will_delete = False
                depth+=1
            if type(getattr(class_instance, attr)) is discord.role.Role:
                props[attr] =  class_to_dict(getattr(class_instance, attr), depth)
                will_delete = False
                depth+=1
            if type(getattr(class_instance, attr)) is list:

                props[attr] = ["bruh"]
            if will_delete:
                props[attr] = ''
        except:
            pass
    for key in props:
        if type(props[key]) is not str and  type(props[key]) is not int and  type(props[key]) is not list and  type(props[key]) is not dict and  type(props[key]) is not float and  type(props[key]) is not bool:
            props[key] = class_to_dict(getattr(class_instance, attr), depth)
        if key.startswith("_"):
            props[key] = ''
       # if type(props[key]) is list :
        #    for i in key:
         #       if type(i) is not str and  type(i) is not int and  type(i) is not list and  type(i) is not dict and  type(i) is not float and  type(i) is not bool:
          #          i = ""


    #props = 
    ##print(str(props))
   # s = jsonpickle.encode(class_instance)
    return str(props)

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
            print(
                "name is",person.name,
                "word is", word
            )
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