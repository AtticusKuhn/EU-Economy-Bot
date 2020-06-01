##this is for the functions that are used many times
import re



def is_role(server_id, role_id):
    server_exists = False
    role_exists = False
    for server in client.guilds:
        if(server.id == server_id)
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
    



def is_user(server_id,user_id):
    server_exists = False
    person_exists = False
    for server in client.guilds:
        if(server.id == server_id)
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



def get_wallet(server_id, ping_wallet):
    server_exists = False
    wallet_exists = False
    for server in client.guilds:
        if(server.id == server_id)
        server_exists = True
        found_server = server
        break
    if(server_exists):
        

    else:
        return (False, "server does not exist")