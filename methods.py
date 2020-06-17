##this is for the functions that are used many times


import re


##finds if a role exists in a server
def is_role(server_id, role_id):
    server_exists = False
    role_exists = False
    for server in client.guilds:
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
    for server in client.guilds:
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



def get_wallet(client, server_id, ping_wallet):
    server_exists = False
    wallet_exists = False
    found_server =""
    print(ping_wallet,"ping_waller")
    for server in client.guilds:
        if(server.id == server_id):
            server_exists = True
            found_server = server
            break
    if(server_exists):
        digit = re.search(r"\d", ping_wallet)
        if digit is not None:
            id_of_wallet = ping_wallet[digit.start():-1]
            print(id_of_wallet)
            for person in found_server.members:
                if str(person.id) == str(id_of_wallet):
                    return (True, person, "person")
            for role in found_server.roles:
                if str(role.id) == str(id_of_wallet):
                    return (True, role, "role")
            return (False, "not found")
        else:
            return (False, "invalid format")
    else:
        return (False, "server does not exist")


def can_access_wallet(client, server_id, person, wallet):
    found_wallet = get_wallet(client, server_id, wallet)
    if(!found_wallet):
        return (False, "can't be found")
    