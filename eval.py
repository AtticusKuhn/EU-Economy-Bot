

from io import StringIO
import sys
import time
from contextlib import contextmanager
import threading
import _thread
import discord
from database import send
import json
import jsonpickle
import discord
import os


code = sys.argv[1]
#json_formatted = sys.argv[2].replace("'",'"')
context = eval(sys.argv[2])
##context_input = eval(context)
# person_roles,server_members,server_roles,person_id
person_roles = eval(sys.argv[3])
server_members = eval(sys.argv[4])
server_roles = eval(sys.argv[5])
person_id = sys.argv[6]



class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        timer.cancel()

def isevaluable(s):
    try:
        exec(s)
        return True
    except:
        return False

def get_eval_error(bad_code):
    try:
        exec(bad_code)
    except Exception as e: return str(e)


class MyClient(discord.Client):
    async def on_ready(self):

        try:
            with time_limit(0.2, 'sleep'):
                if context["type"] == "message":
                    #pass
                    guild= client.get_guild(int(context["guild"]))
                    channel =  guild.get_channel(int(context["channel"]))
                    message = await channel.fetch_message(int(context["message"]))
                if isevaluable(code):
                    codeOut = StringIO()
                    sys.stdout = codeOut 
                    exec(code)
                    sys.stdout = sys.__stdout__
                    step3 = codeOut.getvalue()
                    codeOut.close()
                    #print(step3)
                else:
                    print(f' there was an error: {get_eval_error(code)}')
        except TimeoutException as e:
            codeOut = StringIO()
            sys.stdout = sys.__stdout__
            codeOut.close()
            print("timed out")
        exit(0)


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)