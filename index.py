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
        #Just for development
        if message.author.id != 332312990441406465:
            await message.channel.send(embed=error.gen("You do not have permission to do this!"))
            return
        os.system("cd /opt/MemeHut/MemeHut-Bot/ && killall python3.6 && python3.6 index.py")
        await message.channel.send()
    elif message.content.startswith("!plugin"):
        if args[0] == "msg":
            try:
                try:
                    f = json.loads(open("../Bot-Storage/" + str(message.guild.id) + ".json").read())
                    if f["plugin-msg"] != []:
                        print("hi")
                        msg = await client.get_message(f["plugin-msg"][0], f["plugin-msg"][1])
                        await client.delete_message(msg)

                    if len(args) >= 2:
                        embed = minehut.plugins(f, int(args[1]))
                    else:
                        embed = minehut.plugins(f, 1)

                    msg = await message.channel.send(embed=embed)
                    await msg.add_reaction("\U00002b05")
                    await msg.add_reaction("\U000027a1")

                    f["plugin-msg"] == [msg.channel, str(msg.id)]

                    file = open("../Bot-Storage/" + str(message.guild.id) + ".json", "w")
                    file.write(json.dumps(f, indent=4, sort_keys=True))

                except json.decoder.JSONDecodeError:
                    return error.gen("Your server's file seems to be corrupted, please contact us. \n\n!contact")
            except FileNotFoundError:
                return error.gen("You have not setup your server yet!")

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
