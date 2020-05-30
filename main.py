import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    async def on_message(self, message):
        pass


client = MyClient()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)