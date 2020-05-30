import discord
import json
import commands.py


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    async def on_message(self, message):
        if(message.startswith("$"));
            if(is_valid_command(message)):
                message_array = message.content.split(" ")
                message_command = message_array[0]
                
            else:
                await message.channel.send("not valid command ")


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)