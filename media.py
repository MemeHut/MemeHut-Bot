import discord
import json
import requests
from random import randint as rand

import error

config = json.loads(open("../config.json").read())

TOKEN_GIPHY = config["giphy_token"]

def gif(query):
    t = rand(0, 11)
    r = requests.get("http://api.giphy.com/v1/gifs/translate?api_key=%s&s=%s&weirdness=%s" % (TOKEN_GIPHY, query, t))
    data = json.loads(r.text)
    embed = discord.Embed()
    embed.set_image(url = data["data"]["images"]["downsized_large"]["url"])
    return embed

def insult(amount):
    out = ""
    for i in range(amount):
        r = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=text")
        out += "%s\n\n" % r.text
    embed = discord.Embed(title = "Insults: ", description = "%s" % out, color = 0x38ff5f)
    return embed
