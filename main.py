import discord
import json
import commands.py
import methods.py

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
                if(message_command == "$send"):
                    if(message.guild, send(message_array[1:])):
                        await message.channel.send("the transfer of money was successful")
                    else:
                        await message.channel.send("an error occured in transferring money")
                if(message_commande == "$balance"):
                    if(get_balance(message.guild, message_array[1:])):
                        await message.channel.send(f'the balane is {get_balance(message.guild, message_array[1:])}')
                    else:
                        await message.channel.send("there was an error")
            else:
                await message.channel.send("not valid command ")


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)