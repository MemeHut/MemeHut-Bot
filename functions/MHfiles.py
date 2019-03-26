import discord
import json
import requests
import math

import error
import files

def view(f, dir=""):
    if dir == "":
        r = json.loads(requests.get("https://api.minehut.com/file/" + f["servers"][f["server"]] + "/list/", headers={"Authorization" : f["auth"]}).text)

    if "error" in r.keys():
        return error.gen("The service is down! The most likely cause for this is that your server is offline, start it with the following command. \n\n!start")

    embed = discord.Embed(colour=discord.Colour(0x86aeec))

    for i in r["files"]:
        name = i["name"]
        if i["blocked"] == True:
            value = "Blocked: True"
        else:
            value = "Blocked: False"
        if i["directory"] == True:
            value += "\nDirectory: True"
        else:
            value += "\nDirectory: False"
        embed.add_field(name=name, value=value, inline=False)

    return embed
