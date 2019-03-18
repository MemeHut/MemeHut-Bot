import discord
import json
import requests

import error
import files

def setup(guild):
    try:
        f = open("../Bot-Storage/" + guild + ".json").read()
        return error.gen("This server has already been setup! In order to reset it, run the following command. \n\n!reset")
    except FileNotFoundError:
        embed = discord.Embed(colour=discord.Colour(0x86aeec))
        embed.add_field(name="Message Sent!", value="I have sent you a DM with more information on how to setup the server!")

        #DM Stuff

        return embed

def reset(guild, user):
    f = json.loads(open("../Bot-Storage/" + guild + ".json").read())

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact")

    if user == f["owner"]:
        return setup(guild)
    else:
        return error.gen("You aren't the owner!", "Error")

def plugins(client, message, page=1):
    if len(args) >= 2 and type(int(args[1])) is not int:
        await message.channel.send(embed=error.gen("The page number must be an integer greater than 1!"))
        return "error"

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
    embed.set_author(name="Plugins - Page " + str(page) + )

    for i in range(10 * page):


    msg = await message.channel.send(embed=embed)

    if len(args) >= 2:
        if int(args[1]) >= 2:
            await msg.add_reaction("\U00002b05")

    await msg.add_reaction("\U000027a1")

    f["plugin-msg"] == [msg.channel, str(msg.id)]

    files.write("../Bot-Storage/" + str(message.guild.id) + ".json", json.dumps(f, indent=4, sort_keys=True))

    return msg
