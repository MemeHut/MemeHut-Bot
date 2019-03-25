import discord
import json
import requests

import error
import files

def account(f):
    r = json.loads(requests.get("https://api.minehut.com/user/" + f["id"], headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="General", value="Credits: " + str(r["user"]["credits"]) + "\n", inline=False)

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][0] + "/server_data", headers={"Authorization" : f["auth"]}).text)
    rr = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][1] + "/server_data", headers={"Authorization" : f["auth"]}).text)

    names = [r["server"]["name"], rr["server"]["name"]]
    credits = [r["server"]["credits_per_day"], rr["server"]["credits_per_day"]]

    embed.add_field(name="Server", value=names[0] + "\n" + names[1], inline=True)
    embed.add_field(name="Credits Per Day", value=str(credits[0]) + "\n" + str(credits[1]), inline=True)

    return embed
