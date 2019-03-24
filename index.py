import requests
import os
import discord
import json
import sys

sys.path.insert(0, './functions/')

import plugins
import motd
import setup

import error
import files

config = files.read("../config.json", True)

TOKEN = config["bot_token"]

emailList = {}
pswList = {}
accEmails = {}

serverSelectedOnly = ["!plugins", "!motd", "!install", "!remove", "!purchase"]
ownerOnly = ["!reset", "!server", "!install", "!remove", "!purchase"]

client = discord.Client()

@client.event
async def on_message(message):
    args = message.content.split(" ")
    args.pop(0)

    if message.author == client.user:
        return

    if str(message.channel).startswith("Direct Message with"):
        if str(message.author.id) in emailList.keys():
            pswList.update({str(message.author.id) : [emailList[str(message.author.id)], message.content]})
            emailList.pop(str(message.author.id))
            return
        elif str(message.author.id) in pswList.keys():
            embed = setup.login(str(message.author.id), pswList[str(message.author.id)][0], pswList[str(message.author.id)][1], message.content)
            await message.channel.send(embed=embed)
            pswList.pop(str(message.author.id))
            return

    f = files.read("../Bot-Storage/" + str(message.guild.id) + ".json", True)

    if not message.content.split(" ")[0] in serverSelectedOnly and not message.content.split(" ")[0] in ownerOnly:
        if message.content.startswith("!restart"):
            if message.author.id != 332312990441406465:
                await message.channel.send(embed=error.gen("You do not have permission to do this!"))
                return
            os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall python3.6 && python3.6 index.py")
            await message.channel.send("Restarting...")

        elif message.content.startswith("!help"):
            embed = discord.Embed(colour=discord.Colour(0xab99e8))
            #Help Stuff
            await message.channel.send(embed=embed)

        elif message.content.startswith("!setup"):
            await message.channel.send(embed=await setup.setup(message, str(message.guild.id)))
            emailList.update({str(message.author.id) : str(message.guild.id)})

    elif message.content.split(" ")[0] in ownerOnly and message.content.split(" ")[0] in serverSelectedOnly:
        if f != "FileNotFoundError":
            if str(message.author.id) != f["owner"]:
                return await message.channel.send(embed=error.gen("You aren't the owner!"))
        if f != "FileNotFoundError":
            if f["server"] == 2:
                return await message.channel.send(embed=setup.serverNotSelected(str(message.guild.id)))

        if message.content.startswith("!install"):
            if len(args) >= 2:
                if int(args[1]) < 0:
                    return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                return await message.channel.send(embed=await plugins.install(message, str(message.guild.id), int(args[0])))
            else:
                return await message.channel.send(embed=error.gen("Please specify an ID \n\n!install (id)"))
        elif message.content.startswith("!remove"):
            if len(args) >= 2:
                if int(args[1]) < 0:
                    return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                return await message.channel.send(embed=await plugins.remove(message, str(message.guild.id), int(args[0])))
            else:
                return await message.channel.send(embed=error.gen("Please specify an ID \n\n!remove (id)"))
        elif message.content.startswith("!purchase"):
            if len(args) >= 2:
                if int(args[1]) < 0:
                    return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                return await message.channel.send(embed=await plugins.purchase(message, str(message.guild.id), int(args[1])))
            else:
                return await message.channel.send(embed=error.gen("Please specify an ID \n\n!purchase (id)"))


    elif message.content.split(" ")[0] in ownerOnly:
        if f != "FileNotFoundError":
            if f["server"] == 2:
                return await message.channel.send(embed=setup.serverNotSelected(str(message.guild.id)))

        if message.content.startswith("!server"):
            if len(args) >= 1:
                return await message.channel.send(embed=error.gen("Please specify an index. \n\n!server (index - 0 or 1)"))

            return await message.channel.send(embed=setup.selectServer(str(message.guild.id), int(args[0])))

        if message.content.startswith("!reset"):
            await message.channel.send(embed=setup.reset(str(message.guild.id), str(message.author.id)))

    elif message.content.split(" ")[0] in serverSelectedOnly:
        if f != "FileNotFoundError":
            if f["server"] == 2:
                return await message.channel.send(embed=setup.serverNotSelected(str(message.guild.id)))
        if message.content.startswith("!motd"):
            if args[0] == "view":
                if len(args) > 1:
                    args.pop(0)
                    await message.channel.send(file=motd.view(str(message.guild.id), False, args))
                else:
                    await message.channel.send(file=motd.view(str(message.guild.id)))
        elif message.content.startswith("!plugins"):
            if len(args) >= 2:
                if args[0] == "search":
                    if int(args[1]):
                        page = args[1]
                        args.pop(0)
                        args.pop(0)
                        query = ""
                        for i in args:
                            query = i + " "
                        return await plugins.view(message, int(page), query)
                    else:
                        return await plugins.view(message, 1, query)
            else:
                if len(args) == 1 and int(args[0]) > 0:
                    return await plugins.view(message, int(args[0]))
                else:
                    return await plugins.view(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
