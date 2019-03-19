import discord
import json
import requests
import math
import os

import error
import files

def login(user, guild, email, psw):
    r = requests.post("https://api.minehut.com/users/login", headers={"Content-Type":"application/json"}, data=json.dumps({"username":email,"password":psw}))

    if r == {"error" : "Invalid email/password."}:
        return error.gen("It appears as though you entered incorrect login information, please try again by running the following command in your server. \n\n !setup", "Invalid Login")

def setup(guild):
    f = files.read("../Bot-Storage/" + guild + ".json")

    if f != "FileNotFoundError":
        return error.gen("This server has already been setup! In order to reset it, run the following command. \n\n!reset")

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Message Sent!", value="I have sent you a DM with more information on how to setup the server!")

    embedd = discord.Embed(colour=discord.Colour(0x86aeec))
    embedd.add_field(name="Link your Minehut account", value="In order to link your minehut account, we will ask for your email and password, if you are not comfortable with this, you can read our source code at the link below. https://github.com/MemeHut/MemeHut-Bot \n NOTE: WE WILL NOT STORE ANY PASSWORDS OR EMAILS. \n\nPlease reply to this message with your email, then a message containing your password.")

    return [embed, embedd]

def reset(guild, user):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact")

    if user == f["owner"]:
        os.remove("../Bot-Storage/" + guild + ".json")
        return setup(guild)
    else:
        return error.gen("You aren't the owner!", "Error")

async def plugins(client, message, page=1):
    f = files.read("../Bot-Storage/" + str(message.guild.id) + ".json", True)

    if f == "FileNotFoundError":
        await message.channel.send(embed=error.gen("You have not setup your server yet!"))
        return "error"
    elif f == "JSONDecodeError":
        await message.channel.send(embed=error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact"))
        return "error"

    if f["plugin-msg"] != []:
        msg = await client.get_message(f["plugin-msg"][0], f["plugin-msg"][1])
        await client.delete_message(msg)

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.set_author(name="Plugins - Page " + str(page) + "/" + str(math.ceil(len(r["plugins"]) / 10)))

    for i in range(10 * page):
        if page > 1 and i <= (10 * page) - 10:
            pass
        else:
            name = r["plugins"][i]["name"]
            credits = r["plugins"][i]["credits"]
            if r["plugins"][i]["state"] == "ACTIVE":
                embed.add_field(name=":white_check_mark: " + name, value="Credits: " + str(credits), inline=False)
            elif r["plugins"][i]["state"] == "PURCHASED":
                embed.add_field(name=":x: " + name, value="Credits: " + str(credits), inline=False)
            elif r["plugins"][i]["state"] == "LOCKED":
                embed.add_field(name=":lock: " + name, value="Credits: " + str(credits), inline=False)

    msg = await message.channel.send(embed=embed)

    if page >= 2:
        await msg.add_reaction("\U00002b05")

    if (len(r["plugins"]) / 10) >= page:
        await msg.add_reaction("\U000027a1")

    f["plugin-msg"] = [str(msg.channel), str(msg.id)]

    files.write("../Bot-Storage/" + str(message.guild.id) + ".json", json.dumps(f, indent=4, sort_keys=True))

    return msg
