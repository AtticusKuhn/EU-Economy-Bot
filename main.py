import discord
import json
import commands
import methods
import os 

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    async def on_message(self, message):
        if(message.content.startswith("$")):
            if(commands.is_valid_command(message)):
                message_array = message.content.split(" ")
                message_command = message_array[0]
                if(message_command == "$help"):
                    await message.channel.send('''
                    - $help - shows all commands
                    - $send (ping person) (wallet name) (amount) - sends an amount to a person from that wallet
                    - $request (ping person) (amount) - requests some money from a person which her or she can accept or deny
                    - $tax (ping person) (amount) (wallet name) - if you have the role "taxation" take that amount of money from the person and put it in the wallet
                    - $print (wallet name) (amount) - creates an amount of money in that wallet if you have the role "printer"
                    - $burn (wallet name) (amount) - deletes that much money from a wallet
                    - $balance (wallet name) - returns the amount of money in the wallet
                    - $config (config option) (config setting) - if you have the admin role, configure the bot. 
                    '''
                    )
                if(message_command == "$send"):
                    if(send(message.guild,message_array[1:])):
                        await message.channel.send("the transfer of money was successful")
                    else:
                        await message.channel.send("an error occured in transferring money")
                if(message_command == "$balance"):
                    if(get_balance(message.guild, message_array[1:])):
                        await message.channel.send(f'the balane is {get_balance(message.guild, message_array[1:])}')
                    else:
                        await message.channel.send("there was an error")
            else:
                await message.channel.send("not valid command ")


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)