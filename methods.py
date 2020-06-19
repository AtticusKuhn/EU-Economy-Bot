##this is for the functions that are used many times


import re
import inspect

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
    print("ping_wallet is", ping_wallet)
    server_exists = False
    wallet_exists = False
    found_server =""
    #print(ping_wallet,"ping_waller")
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
        print(id_of_wallet, "is id_of_wallet")
        for person in server_members:
            print(str(person), str(id_of_wallet))
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
    print("found_wallet is",found_wallet)
    if(not found_wallet[0]):
        return False
    print(str(found_wallet[1]),str(person_id) )
    if(str(found_wallet[1]) == str(person_id)):
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
        return True
    return False

    
def class_to_dict(class_instance):
    props = {}
    for attr in dir(class_instance):
        called =True
        try:
            if not callable(getattr(class_instance, attr)):
                called = False
        except:
            pass
        if not called:
            if not attr.startswith("_") and getattr(class_instance, attr) is not None:
                print(callable(getattr(class_instance, attr)))
                print("the attr is",attr, not attr.startswith("_"))
                print("getattr is",  getattr(class_instance, attr))
                print(type(getattr(class_instance, attr)))
                if  str(getattr(class_instance, attr)).startswith("<"): #or getattr(class_instance, attr).startswith("<") : 
                    if type(getattr(class_instance, attr)) is not list:
                        props[attr] = class_to_dict(getattr(class_instance, attr))
                        print("adding to 1")
                else: #not callable(getattr(class_instance, attr))# and not attr.startswith("_"):
                    props[attr] = getattr(class_instance, attr)
                    print("attr is",getattr(class_instance, attr))              
    
    for key in props:
        if type(props[key]) is not str or type(props[key]) is not bool or type(props[key]) is not dict or type(props[key]) is not list or type(props[key]) is not int:
            props[key] = ""
    props = str(props)
    props.replace("<",'"')
    props.replace("<",'"')
    props.replace(">",'"')
    props.replace(">",'"')
    print("final result is", props)
    return props