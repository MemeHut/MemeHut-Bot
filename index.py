import requests
import os
import discord
import json
import sys

sys.path.insert(0, './functions/')

import plugins
import motd
import setup
import controls

import error
import files
import checks

config = files.read("../config.json", True)

TOKEN = config["bot_token"]

devs = [332312990441406465]

emailList = {}
pswList = {}
accEmails = {}

serverSelectedOnly = ["!plugins", "!motd", "!install", "!remove", "!purchase"]
ownerOnly = ["!reset", "!server", "!install", "!remove", "!purchase", "!stop", "!start"]

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    cmd = message.content.split(" ")[0]
    args = message.content.split(" ")
    args.pop(0)
    channel = message.channel

    uid = message.author.id
    if str(channel).startswith("Direct Message with"):
        f = files.read("../Bot-Storage/dm-" + str(message.author.id) + ".json", True)
        id = str(message.author.id)
    else:
        f = files.read("../Bot-Storage/" + str(message.guild.id) + ".json", True)
        id = str(message.guild.id)

    if f == "JSONDecodeError":
        return await channel.send(embed=error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset"))

    if str(channel).startswith("Direct Message with"):
        if str(uid) in emailList.keys():
            pswList.update({str(uid) : [emailList[str(uid)], message.content]})
            return emailList.pop(str(uid))
        elif str(uid) in pswList.keys():
            await channel.send(embed=setup.login(uid, pswList[str(uid)][0], pswList[str(uid)][1], message.content))
            return pswList.pop(str(uid))

    if cmd == "!setup":
        await channel.send(embed=await setup.setup(message, f))
        return emailList.update({str(uid) : id})
    elif cmd == "!help":
            embed = discord.Embed(colour=discord.Colour(0xab99e8))
            #Help Stuff
            await channel.send(embed=embed)
    elif cmd == "!restart":
        if uid not in devs:
            return await channel.send(embed=error.gen("You do not have permission to do this!"))
        await channel.send("Restarting...")
        return os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall python3.6 && python3.6 index.py")

    if f == "FileNotFoundError":
        return await channel.send(embed=error.gen("You have not setup your server yet!"))

    if cmd in ownerOnly and cmd in serverSelectedOnly:
        if uid != f["owner"]:
            return await channel.send(embed=error.gen("You aren't the owner!"))
        if f["server"] == 2:
            return await channel.send(embed=setup.serverNotSelected(f))

        if cmd == "!install":
            if args != []:
                if checks.isInt(args[0]):
                    if int(args[0]) < 0:
                        return await channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await channel.send(embed=plugins.install(f, int(args[0])))
                else:
                    return await channel.send(embed=error.gen("The value " + args[0] + " is not an integer."))
            else:
                return await channel.send(embed=error.gen("Please specify an ID \n\n!install (id)"))
        elif cmd == "!remove":
            if args != []:
                if checks.isInt(args[0]):
                    if int(args[0]) < 0:
                        return await channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await channel.send(embed=plugins.remove(f, int(args[0])))
                else:
                    return await channel.send(embed=error.gen("The value " + args[0] + " is not an integer."))
            else:
                return await channel.send(embed=error.gen("Please specify an ID \n\n!remove (id)"))
        elif cmd == "!purchase":
            if args != []:
                if checks.isInt(args[0]):
                    if int(args[0]) < 0:
                        return await channel.send(embed=error.gen("The plugin ID must be greater than or equal to 0!"))
                    return await channel.send(embed=plugins.purchase(f, int(args[0])))
                else:
                    return await channel.send(embed=error.gen("The value " + args[0] + " is not an integer."))
            else:
                return await channel.send(embed=error.gen("Please specify an ID \n\n!purchase (id)"))
    elif cmd in ownerOnly:
        if uid != f["owner"]:
            return await channel.send(embed=error.gen("You aren't the owner!"))
        if cmd == "!server":
            if args != []:
                return await channel.send(embed=error.gen("Please specify an index. \n\n!server (index - 0 or 1)"))
            if not checks.isInt(args[0]):
                return await channel.send(embed=error.gen("The value " + args[0] + " is not an integer."))
            return await channel.send(embed=setup.selectServer(f, int(args[0])))
        elif cmd == "!reset":
            await channel.send(embed=setup.reset(str(message.guild.id), str(message.author.id)))
        elif cmd == "!stop":
            return await channel.send(embed=controls.stop(f))
        elif cmd == "!start":
            return await channel.send(embed=controls.start(f))
    elif cmd in serverSelectedOnly:
        if cmd == "!motd":
            if args[0] == "view":
                if len(args) > 1:
                    args.pop(0)
                    return await channel.send(file=motd.view(f, False, args))
                else:
                    return await channel.send(file=motd.view(f))
        elif cmd == "!plugins":
            if len(args) >= 2:
                if args[0] == "search":
                    args.pop(0)
                    if checks.isInt(args[0]):
                        page = int(args[0])
                        args.pop(0)
                        query = ""
                        for i in args:
                            query = i + " "
                        return await channel.send(embed=plugins.view(f, page, query))
                    else:
                        args.pop(0)
                        query = ""
                        for i in args:
                            query = i + " "
                        return await channel.send(embed=plugins.view(f, 1, query))
            else:
                if args != []:
                    if checks.isInt(args[0]):
                        return await channel.send(embed=plugins.view(f, int(args[0])))
                    else:
                        return await channel.send(embed=error.gen("The value " + args[0] + "is not an integer."))
                else:
                    return await channel.send(embed=plugins.view(f))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
