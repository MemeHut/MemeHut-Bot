import discord
import json
import requests

def gen(m, t="Error"):
    embed = discord.Embed(title=t, description=m, color=0xfc4444)
    return embed
