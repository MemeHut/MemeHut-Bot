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

serverSelectedOnly = ["!plugins"]
ownerOnly = ["!plugins", "!reset", "!server"]

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

        if message.content.startswith("!plugins"):
            if args[0] == "view":
                if len(args) >= 2 and int(args[1]) > 0:
                    msg = await plugins.view(client, message, int(args[1]))
                else:
                    msg = await plugins.view(client, message)
            elif args[0] == "install":
                if len(args) >= 2:
                    if int(args[1]) < 0:
                        return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await message.channel.send(embed=await plugins.install(message, str(message.guild.id), int(args[1])))
                else:
                    return await message.channel.send(embed=error.gen("Please specify an ID \n\n!plugins install (id)"))
            elif args[0] == "remove":
                if len(args) >= 2:
                    if int(args[1]) < 0:
                        return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await message.channel.send(embed=await plugins.remove(message, str(message.guild.id), int(args[1])))
                else:
                    return await message.channel.send(embed=error.gen("Please specify an ID \n\n!plugins remove (id)"))
            elif args[0] == "purchase":
                if len(args) >= 2:
                    if int(args[1]) < 0:
                        return await message.channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await message.channel.send(embed=await plugins.purchase(message, str(message.guild.id), int(args[1])))
                else:
                    return await message.channel.send(embed=error.gen("Please specify an ID \n\n!plugins purchase (id)"))


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
            if args == None:
                await message.channel.send(embed=motd.view(str(message.guild.id))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
