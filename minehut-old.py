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

def pluginGen(f, page=1):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.set_author(name="Plugins - Page " + str(page))

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

    return embed

async def plugins(client, message, args):
    try:
        try:
            if len(args) >= 2:
                if type(int(args[1])) is not int:
                   await message.channel.send(embed=error.gen("The page number must be an integer greater than 1!"))
                   return "error"

            f = json.loads(open("../Bot-Storage/" + str(message.guild.id) + ".json").read())
            if f["plugin-msg"] != []:
                msg = await client.get_message(f["plugin-msg"][0], f["plugin-msg"][1])
                await client.delete_message(msg)

            if len(args) >= 2:
                embed = pluginGen(f, int(args[1]))
            else:
                embed = pluginGen(f, 1)

            msg = await message.channel.send(embed=embed)
            if len(args) >= 2:
                if int(args[1]) >= 2:
                    await msg.add_reaction("\U00002b05")

            await msg.add_reaction("\U000027a1")

            f["plugin-msg"] == [msg.channel, str(msg.id)]

            file = open("../Bot-Storage/" + str(message.guild.id) + ".json", "w")
            file.write(json.dumps(f, indent=4, sort_keys=True))

            return msg

        except json.decoder.JSONDecodeError:
            await message.channel.send(embed=error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact"))
            return "error"
    except FileNotFoundError:
        await message.channel.send(embed=error.gen("You have not setup your server yet!"))
        return "error"
