import requests
import os
import discord
import json
import sys

sys.path.insert(0, './functions/')

import plugins
import setup

import error
import files

config = files.read("../config.json", True)

TOKEN = config["bot_token"]

emailList = {}
pswList = {}
accEmails = {}

serverNotSelected = ["!plugins", "!setup", "!reset"]

client = discord.Client()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if str(message.channel).startswith("Direct Message with"):
        if str(message.author.id) in emailList.keys():
            pswList.update({str(message.author.id) : [emailList[str(message.author.id)], str(message.content)]})
            emailList.pop(str(message.author.id))

        elif str(message.author.id) in pswList.keys():
            embed = setup.login(str(message.author.id), pswList[str(message.author.id)][0], pswList[str(message.author.id)][1], str(message.content))

            await message.channel.send(embed=embed)

            pswList.pop(str(message.author.id))

    args = message.content.split(" ")
    args.pop(0)

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

    elif message.content.split(" ")[0] in serverNotSelected:

        if message.content.startswith("!setup"):
            embed = await setup.setup(message, str(message.guild.id))
            return await message.channel.send(embed=embed)

            emailList.update({str(message.author.id) : str(message.guild.id)})

        # Here starts ownership required commands

        f = files.read("../Bot-Storage/" + str(message.guild.id) + ".json", True)

        if f != "FileNotFoundError":
            if str(message.author.id) != f["owner"]:
                 return await message.channel.send(embed=error.gen("You aren't the owner!"))

        if message.content.startswith("!server"):
            print(args)
            if args[0] == None:
                return await message.channel.send(embed=error.gen("Please specify an index. \n\n!server (index - 0 or 1)"))

            embed = setup.selectServer(str(message.guild.id), int(args[0]))

            await message.channel.send(embed=embed)

        #Can't run without server selected

        if f != "FileNotFoundError":
            if f["server"] == 2:
                embed = setup.serverNotSelected(str(message.guild.id))
                return await message.channel.send(embed=embed)

        if message.content.startswith("!reset"):
            embed = await setup.reset(str(message.guild.id), str(message.author.id))
            await message.channel.send(embed=embed)

        elif message.content.startswith("!plugins"):
            if args[0] == "view":
                if len(args) >= 2 and int(args[1]) > 0:
                    msg = await plugins.view(client, message, int(args[1]))
                else:
                    msg = await plugins.view(client, message)

                if msg == "error":
                    return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
