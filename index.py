import requests
import os
import discord
import json
import procname

procname.setprocname("MemeHut-Bot")

import media
import error
import minehut

config = files.read("../config.json", True)

TOKEN = config["bot_token"]

client = discord.Client()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    args = message.content.split(" ")
    args.pop(0)

    if message.content.startswith("!setup"):
        embed = minehut.setup(str(message.guild.id))
        await message.channel.send(embed=embed)
    elif message.content.startswith("!reset"):
        embed = minehut.reset(str(message.guild.id), str(message.author.id))
        await message.channel.send(embed=embed)
    elif message.content.startswith("!restart"):
        if message.author.id != 332312990441406465:
            await message.channel.send(embed=error.gen("You do not have permission to do this!"))
            return
        os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall MemeHut-Bot && python3.6 index.py")
        await message.channel.send("Restarting... ")
    elif message.content.startswith("!plugin"):
        if args[0] == "msg":
            if len(args) >= 2 and int(args[1]) > 0:
                msg = await minehut.plugins(client, message, int(args[1]))
            else:
                msg = await minehut.plugins(client, message)

            if msg == "error":
                return

    elif message.content.startswith("!help"):
        embed = discord.Embed(colour=discord.Colour(0xab99e8))

        #Help Stuff
        
        await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
