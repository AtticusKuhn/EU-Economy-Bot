import discord
from config import config
from datetime import date

def simple_embed(success,message):
    if success=="info":
        color=0x0000ff
    if success:
        color=0x00ff00
    if not success:
        color=0xff0000
    embedVar = discord.Embed(
        title="EU Economy Bot",
        description=message,
        color=color,
        url=config["website"]
    )
    embedVar.set_footer(text="A general purpose economy bot", icon_url=config["image"])
    #embedVar.set_thumbnail(config["image"])
    return embedVar