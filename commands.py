commands_array = [
    ("$send",3),
    ("$request",2)
]
def is_valid_command(user_message):
    user_array = user_message.split(" ")
    for command in commands_array:
        if(command[0] == user_array[0] and command[1]==len(user_array)-1 ):
            return True
    return False
