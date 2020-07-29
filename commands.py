##this file handles commands

commands_array = [
    ("$help",0),
    ("$send",3),
   #######  ("$request",2),
   ("$create",1),
   ("$balance",1),
   ("$print",2),
   ("$dev-db",0),
   ("$clear-contracts",0),
   ("$links",0),
   ("$config",2),
   ("$stats",1),
   ("$whois", "any"),
   ("$send-each", "any"),
   ("$set-balance", 2),
   ("$alter-balance", 2),
   ("$set-balance-each", "any"),
   ("$wallet-settings", 4),
   ("$trade","any"),
   ("$accept",2)
   ]
def is_valid_command(user_message):
    user_array = user_message.content.split(" ")
    for command in commands_array:
        if(command[0] == user_array[0]):
            if(command[1]==len(user_array)-1  or command[1] == "any" ):
                return True
    return False
