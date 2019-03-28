import discord
import json
import requests
import math

import error
import files

def view(f, dir=""):
    dir = dir.replace(">", "/")

    r = json.loads(requests.get("https://api.minehut.com/file/" + f["servers"][f["server"]] + "/list/" + dir, headers={"Authorization" : f["auth"]}).text)
    if "error" in r.keys():
        return error.gen("The service is down! The most likely cause for this is that your server is offline, start it with the following command. \n\n!start")

    embed = discord.Embed(colour=discord.Colour(0x86aeec))

    value = "<:vertical_line:560136222517886979>\n"
    for i in r["files"]:
        if i["directory"] == True:
            value += "<:l_line:560137261782532135>:file_folder: " + i["name"] + "/\n"
        else:
            value += "<:l_line:560137261782532135><:file:560628181984608256> " + i["name"] + "\n"

    embed.add_field(name="Files - root/" + dir, value=value)

    return embed
