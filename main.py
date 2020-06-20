#modules
import discord
import json
import os
import re
import threading
os.system("pip install dnspython")

#files
import database 
import methods
import commands
import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        for guild in self.guilds:
            print(guild)
            time_trigger_msg = methods.set_interval( database.trigger_time,1, guild, client)

    async def on_message(self, message):
        person_roles= list(map(lambda role: role.id , message.author.roles))
        server_members = list(map(lambda member:member.id, message.guild.members))
        server_roles = list(map(lambda role: role.id, message.guild.roles))
        person_id = message.author.id
        if(message.author.bot):
            return
        ##(guild, message,  person_roles,server_members,server_roles,person_id)
        trigger_msg = database.trigger_messages(message.guild, message, person_roles, server_members, server_roles, message.author.id)
        #print(trigger_msg)
        for i in trigger_msg:
            if(i[1]):
                if(not i[0]):
                    await message.channel.send(f'<@!{i[2]}> your smart contract was annuled: {i[1]}')
                else:
                    await message.channel.send(f'<@!{i[2]}> your smart contract said: {i[1]}')
            
        if(message.content.startswith("$")):
            if(message.content.startswith("$smart-contract")):
                if(message.content.count("```") == 2):
                    if(message.content.split("```")[0].count(" ") == 2):
                        await message.channel.send(database.write_contract(message.guild,message.author,message.content.split("```")[1],message.content.split(" ")[1],client, person_roles,server_members,server_roles,person_id  )[1])
                        return
            if(commands.is_valid_command(message)):
                message_array = message.content.split(" ")
                message_command = message_array[0]
                if(message_command == "$help"):
                    await message.channel.send('''
- $help - shows all commands
- $send (ping person) (wallet name) (amount) - sends an amount to a person from that wallet
- $print (wallet name) (amount) - creates an amount of money in that wallet if you have the role "printer"
- $balance (wallet name) - returns the amount of money in the wallet
- $links - show some links related to this bot
- $smart-contract (trigger) (code block) - code a smart contract
- $clear-contracts - delete all your smart contracts.
                    '''
                    )
                if(message_command == "$send"):
                    #send(person_roles, server_members, server_roles, person_id, guild_id, from_wallet, to_wallet, amount)
                    person_roles= list(map(lambda role: role.id , message.author.roles))
                    server_members = list(map(lambda member:member.id, message.guild.members))
                    server_roles = list(map(lambda role: role.id, message.guild.roles))

                    send_result = database.send(person_roles,server_members, server_roles, message.author.id, message.guild.id, message_array[1], message_array[2], message_array[3])
                    if  send_result[0]:
                        await message.channel.send("success")
                    else:
                        await message.channel.send(f'an error occured {send_result[1]}')
                if(message_command == "$create"):
                    result = database.create(message.guild.id, message_array[1], server_members, server_roles,client)
                    if(result[0]):
                        await message.channel.send("created")
                    else:
                        await message.channel.send(f'error {result[1]}')
                if(message_command == "$balance"):
                    ##guild,wallet,server_members, server_roles
                    if(database.get_balance(message.guild.id, message_array[1],server_members, server_roles)[0]):
                        await message.channel.send(f'the balance is {database.get_balance(message.guild.id, message_array[1],server_members, server_roles)[1]["balance"]}')
                    else:
                        await message.channel.send("there was an error")
                if(message_command == "$print"):
                    roles = map(lambda role: role.name, message.author.roles)
                    if("printer" not in roles):
                        await message.channel.send("you do not have the role printer")
                        return
                    ##(discord_client, guild_id, wallet, amount)
                    result = database.print_money(server_members,server_roles, client, message.guild.id, message_array[1], message_array[2])
                    if(result[0]):
                        await message.channel.send("the printing was successful")
                    else:
                        await message.channel.send(f' there was an error {result[1]}')
                if(message_command == "$clear-contracts"):
                    database.clear_contracts(message.guild, message.author.id)
                    await message.channel.send("your contracts were all deleted")
                if(message_command == "$links"):
                    await message.channel.send("Github - https://github.com/eulerthedestroyer/EU-Economy-Bot \n Discord link - https://discord.gg/KfDjUz \n Bot link - https://discord.com/oauth2/authorize?scope=bot&client_id=716434826151854111")
                if(message_command == "$config"):
                    if message.author.guild_permissions.administrator:
                        await message.channel.send(database.set_config(message.guild ,message_array[1], message_array[2]))
                    else:
                        await message.channel.send("you must be an administrator to access the config")
            else:
                await message.channel.send("not valid command ")


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)