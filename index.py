import requests
import os
import discord
import json

import media
import error
import minehut
import files

config = files.read("../config.json", True)

TOKEN = config["bot_token"]
emailList = {}
pswList = {}
accEmails = {}

client = discord.Client()

@client.event
async def on_message(message):

    if str(message.channel).startswith("Direct Message with"):
        if str(message.author.id) in emailList.keys():
            pswList.update({str(message.author.id) : [emailList[str(message.author.id)], str(message.content)]})
            emailList.pop(str(message.author.id))
            
        elif str(message.author.id) in pswList.keys():
            embed = minehut.login(str(message.author.id), pswList[str(message.author.id)][0], pswList[str(message.author.id)][1], str(message.content))
            

    if message.author == client.user:
        return

    args = message.content.split(" ")
    args.pop(0)

    if message.content.startswith("!setup"):
        embeds = minehut.setup(str(message.guild.id))
        await message.channel.send(embed=embeds[0])

        await message.author.send(embed=embeds[1])

        emailList.update({str(message.author.id) : str(message.guild.id)})

    elif message.content.startswith("!reset"):
        embed = minehut.reset(str(message.guild.id), str(message.author.id))
        await message.channel.send(embed=embed)
    elif message.content.startswith("!restart"):
        if message.author.id != 332312990441406465:
            await message.channel.send(embed=error.gen("You do not have permission to do this!"))
            return
        os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall python3.6 && python3.6 index.py")
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
