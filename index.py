import requests
import os
import discord
import json

import media
import error
import minehut

config = json.loads(open("../config.json").read())

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
        os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall python3 && python3 index.py")
        await message.channel.send("Restarting... ")
    elif message.content.startswith("!plugin"):
        if args[0] == "msg":
            msg = await minehut.plugins(client, message, args)

            if msg == "error":
                return

            res = client.wait_for_reaction(["\U00002b05", "\U000027a1"], message=msg)
            if res.reaction.emoji == "\U00002b05":
                print("hoi")
            else:
                print("no")

    elif message.content.startswith("!help"):
        embed = discord.Embed(colour=discord.Colour(0xab99e8))

        embed.add_field(name="View Fortnite Stats", value="!stats (username) (platform - XBOX, PC, PS)", inline=False)
        embed.add_field(name="View Fortnite Match History", value="!matches (username) (platform - XBOX, PC, PS)", inline=False)
        embed.add_field(name="View Current Fortnite Item Shop", value="!store", inline=False)
        embed.add_field(name="Search Giphy For a Gif", value="!gif (search)\ne.g - !gif cats", inline=False)
        embed.add_field(name="Generate Insults", value="!insult (amount)", inline=False)

        await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
