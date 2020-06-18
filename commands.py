##this file handles commands


commands_array = [
    ("$help",0),
    ("$send",3),
   #######  ("$request",2),
   ("$create",1),
   ("$balance",1),
   ("$print",2),
   ("$dev-db",0),
   ("$clear-contracts",0)
   ]
def is_valid_command(user_message):
    user_array = user_message.content.split(" ")
    for command in commands_array:
        if(command[0] == user_array[0] and command[1]==len(user_array)-1 ):
            return True
    return False
