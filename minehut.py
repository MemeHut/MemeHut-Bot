import discord
import json
import requests

import error

def setup(guild):
    try:
        f = open("../Bot-Storage/" + guild + ".json").read()
        return error.gen("This server has already been setup! In order to reset it, run the following command. \n\n!reset")
    except FileNotFoundError:
        embed = discord.Embed(colour=discord.Colour(0x86aeec))
        embed.add_field(name="Message Sent!", value="I have sent you a DM with more information on how to setup the server!")
        return embed

def reset(guild, user):
        try:
            try:
                f = json.loads(open("../Bot-Storage/" + guild + ".json").read())
                if user == f["owner"]:
                    return error.gen("Hi Owner", "Spanks")
                else:
                    return error.gen("You aren't the owner!", "Error")
            except json.decoder.JSONDecodeError:
                return error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact")
        except FileNotFoundError:
            print("h")

def plugins(f, page):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.set_author(name="Plugins - Page " + str(page))

    for i in range(10 * page):
        if page > 1 and i < 10 * page:
    pass
        name = r["plugins"][i]["name"]
        credits = r["plugins"][i]["credits"]
        if r["plugins"][i]["state"] == "ACTIVE":
            embed.add_field(name=":white_check_mark: " + name, value="Credits: " + str(credits), inline=False)
        elif r["plugins"][i]["state"] == "PURCHASED":
            embed.add_field(name=":x: " + name, value="Credits: " + str(credits), inline=False)
        elif r["plugins"][i]["state"] == "LOCKED":
            embed.add_field(name=":lock: " + name, value="Credits: " + str(credits), inline=False)

    return embed
