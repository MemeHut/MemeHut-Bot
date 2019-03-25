import discord
import json
import requests
import math

import error
import files

def start(f):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)
    if r["status"]["online"] == True:
        return error.gen("Your server is already online!")

    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/start_service", headers={"Authorization" : f["auth"]})

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Starting server.", value="Your server is starting up.", inline=False)

    return embed

def stop(f):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)
    if r["status"]["online"] == False:
        return error.gen("Your server is already offline!")

    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/shutdown", headers={"Authorization" : f["auth"]})

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Stopping server.", value="Your server is stopping.", inline=False)

    return embed

def status(f):
    embed = discord.Embed(colour=discord.Colour(0x86aeec))

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)

    embed.add_field(name="Server Status", value="Status: " + r["status"]["status"] + "\nPlayers: " + str(r["status"]["player_count"]) + "/" + str(r["status"]["max_players"]), inline=False)

    return embed
