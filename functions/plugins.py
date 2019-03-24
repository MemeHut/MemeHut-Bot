import discord
import json
import requests
import math

import error
import files

async def view(message, page=1, query=""):
    f = files.read("../Bot-Storage/" + str(message.guild.id) + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset")
    
    if f["plugin-msg"] != "":
        msg = await message.channel.fetch_message(f["plugin-msg"])
        await msg.delete()

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))

    numOfPlugins = 0
    for i in range(len(r["plugins"])):
        name = r["plugins"][i]["name"]
        credits = r["plugins"][i]["credits"]
        if query == "":
            if i <= 10 * page and i >= (10 * page) - 10 and i <= len(r["plugins"]) - 1:
                if r["plugins"][i]["state"] == "ACTIVE":
                    embed.add_field(name="<:installed:559156765833429032> " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
                elif r["plugins"][i]["state"] == "PURCHASED":
                    embed.add_field(name="<:uninstalled:559156765569056789>  " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
                elif r["plugins"][i]["state"] == "LOCKED":
                    embed.add_field(name="<:locked:559156765816651786> " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
        else:
            if query.lower() in name.lower():
                if numOfPlugins <= 9 * page and numOfPlugins >= (9 * page) - 9 and i <= len(r["plugins"]) - 1:
                    if r["plugins"][i]["state"] == "ACTIVE":
                        embed.add_field(name="<:installed:559156765833429032> " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
                    elif r["plugins"][i]["state"] == "PURCHASED":
                        embed.add_field(name="<:uninstalled:559156765569056789>  " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
                    elif r["plugins"][i]["state"] == "LOCKED":
                        embed.add_field(name="<:locked:559156765816651786> " + name, value="Credits: " + str(credits) + "\nID: " + str(i), inline=False)
                numOfPlugins = numOfPlugins + 1

    if query != "":
        numOfPages = 0
        for i in range(len(r["plugins"])):
            name = r["plugins"][i]["name"]
            if query.lower() in name.lower():
                numOfPages = numOfPages + 1

        numOfPages = math.ceil(numOfPages / 10)
        embed.set_author(name="Plugins - Page " + str(page) + "/" + str(numOfPages))
    else:
        embed.set_author(name="Plugins - Page " + str(page) + "/" + str(math.ceil(len(r["plugins"]) / 10)))

    msg = await message.channel.send(embed=embed)

    """
    if page > 1:
        await msg.add_reaction("\U00002b05")

    if math.ceil(len(r["plugins"]) / 10) - 1 >= page:
        await msg.add_reaction("\U000027a1")

    """
    f["plugin-msg"] = str(msg.id)

    files.write("../Bot-Storage/" + str(message.guild.id) + ".json", json.dumps(f, indent=4, sort_keys=True))

def install(guild, id):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset")

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    if id > len(r["plugins"]) - 1:
        return error.gen("The plugin ID you entered is too high, there aren't that many plugins!")

    pluginID = r["plugins"][id]["_id"]
    pluginName = r["plugins"][id]["name"]

    if r["plugins"][id]["state"] == "ACTIVE":
        return error.gen("The plugin " + pluginName + " is already installed on this server! If you would like to remove it, run the following command.\n\n!plugins remove " + str(id))
    elif r["plugins"][id]["state"] == "LOCKED":
        return error.gen("The plugin " + pluginName + " is locked, if you want to install it, you will have to purchase it.\n\n!plugins purchase (id)")

    rr = json.loads(requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/install_plugin", headers={"Authorization" : f["auth"]}, data=json.dumps({"plugin" : pluginID})).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Plugin installed!", value="Succesfully installed the plugin " + pluginName, inline=False)

    return embed

def remove(guild, id):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset")

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    if id > len(r["plugins"]) - 1:
        return error.gen("The plugin ID you entered is too high, there aren't that many plugins!")

    pluginID = r["plugins"][id]["_id"]
    pluginName = r["plugins"][id]["name"]

    if r["plugins"][id]["state"] == "PURCHASED" or r["plugins"][id]["state"] == "LOCKED":
        return error.gen("The plugin " + pluginName + " is not installed on this server! If you would like to install it, run the following command.\n\n!plugins install " + str(id))

    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/remove_plugin", headers={"Authorization" : f["auth"], "Content-Type" : "application/json"}, data=json.dumps({"plugin" : pluginID}))

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Plugin removed!", value="Succesfully removed the plugin " + pluginName, inline=False)

    return embed

def purchase(guild, id):
    f = files.read("../Bot-Storage/" + guild + ".json", True)

    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset")

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"], "Content-Type" : "application/json"}).text)

    if id > len(r["plugins"]) - 1:
        return error.gen("The plugin ID you entered is too high, there aren't that many plugins!")

    pluginID = r["plugins"][id]["_id"]
    pluginName = r["plugins"][id]["name"]

    if r["plugins"][id]["state"] == "ACTIVE" or r["plugins"][id]["state"] == "PURCHASED":
        return error.gen("You already own the plugin " + pluginName)

    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/purchase_plugin", headers={"Authorization" : f["auth"], "Content-Type" : "application/json"}, data=json.dumps({"plugin" : pluginID}))
    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/install_plugin", headers={"Authorization" : f["auth"], "Content-Type" : "application/json"}, data=json.dumps({"plugin" : pluginID}))

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Plugin purchased and installed!", value="Succesfully purchased and installed the plugin " + pluginName, inline=False)

    return embed
