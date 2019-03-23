import discord
import json
import requests
import os

import error
import files

def login(user, guild, email, psw):
    r = json.loads(requests.post("https://api.minehut.com/users/login", headers={"Content-Type":"application/json"}, data=json.dumps({"email":email,"password":psw})).text)

    data = files.read("../Bot-Storage/template.json", True)

    data["auth"] = r["token"]
    data["servers"][0] = r["servers"][0]
    data["servers"][1] = r["servers"][1]
    data["owner"] = user

    files.write("../Bot-Storage/" + guild + ".json", json.dumps(data, indent=4, sort_keys=True))

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Server Setup!", value="Your server has been setup! For a list of commands run the following command. \n\n!help")

    return embed

async def setup(message, guild):
    f = files.read("../Bot-Storage/" + guild + ".json")

    if f != "FileNotFoundError":
        return error.gen("This server has already been setup! In order to reset it, run the following command. \n\n!reset")

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Message Sent!", value="I have sent you a DM with more information on how to setup the server!")

    embedd = discord.Embed(colour=discord.Colour(0x86aeec))
    embedd.add_field(name="Link your Minehut account", value="In order to link your minehut account, we will ask for your email and password, if you are not comfortable with this, you can read our source code at the link below.\nNOTE: WE WILL NOT STORE ANY PASSWORDS OR EMAILS. \nhttps://github.com/MemeHut/MemeHut-Bot \n\nPlease reply to this message with your email, then a message containing your password.")

    await message.author.send(embed=embedd)

    return embed

def reset(guild, user):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact")

    if user == f["owner"]:
        os.remove("../Bot-Storage/" + guild + ".json")

        embed = discord.Embed(colour=discord.Colour(0x86aeec))
        embed.add_field(name="Server Reset!", value="Your server has been reset.")

        return embed
    else:
        return error.gen("You aren't the owner!")

def serverNotSelected(guild):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][0] + "/server_data", headers={"Authorization" : f["auth"]}).text)
    rr = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][1] + "/server_data", headers={"Authorization" : f["auth"]}).text)

    names = [r["server"]["name"], rr["server"]["name"]]

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="One last step!", value="You have more than one server on your Minehut account, you need to select one. \n\nYou have the following servers: \n0. " + names[0] + "\n1. " + names[1] + "\n\n Please run the following command. \n\n!server (index - 0 or 1)")

    return embed


def selectServer(guild, index):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    f["server"] = index

    files.write("../Bot-Storage/" + guild + ".json", json.dumps(f, indent=4, sort_keys=True))

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Setup complete!", value="Your server is now completely setup! Run the following command for a list of commands. \n\n!help")

    return embed
