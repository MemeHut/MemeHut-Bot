import discord
import json
import requests
import math

import error
import files

def view(f, page=1, query=""):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    embed = discord.Embed(colour=discord.Colour(0x86aeec))

    numOfPlugins = 0
    for i in range(len(r["plugins"])):
        name = r["plugins"][i]["name"]
        credits = r["plugins"][i]["credits"]
        if query == "":
            if i <= 9 * page and i >= (9 * page) - 9 and i <= len(r["plugins"]) - 1:
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

        numOfPages = math.ceil(numOfPages / 9)
        embed.set_author(name="Plugins - Page " + str(page) + "/" + str(numOfPages))
    else:
        embed.set_author(name="Plugins - Page " + str(page) + "/" + str(math.ceil(len(r["plugins"]) / 9)))

    return embed

def install(f, id):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)
    if r["status"]["online"] == False:
        return error.gen("Your server is offline! Start it in order to manage plugins.")

    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/plugins", headers={"Authorization" : f["auth"]}).text)

    if id > len(r["plugins"]) - 1:
        return error.gen("The plugin ID you entered is too high, there aren't that many plugins!")

    pluginID = r["plugins"][id]["_id"]
    pluginName = r["plugins"][id]["name"]

    if r["plugins"][id]["state"] == "ACTIVE":
        return error.gen("The plugin " + pluginName + " is already installed on this server! If you would like to remove it, run the following command.\n\n!plugins remove " + str(id))
    elif r["plugins"][id]["state"] == "LOCKED":
        return error.gen("The plugin " + pluginName + " is locked, if you want to install it, you will have to purchase it.\n\n!plugins purchase (id)")

    requests.post("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/install_plugin", headers={"Authorization" : f["auth"]}, data=json.dumps({"plugin" : pluginID}))

    embed = discord.Embed(colour=discord.Colour(0x86aeec))
    embed.add_field(name="Plugin installed!", value="Succesfully installed the plugin " + pluginName, inline=False)

    return embed

def remove(f, id):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)
    if r["status"]["online"] == False:
        return error.gen("Your server is offline! Start it in order to manage plugins.")
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

def purchase(f, id):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/status", headers={"Authorization" : f["auth"]}).text)
    if r["status"]["online"] == False:
        return error.gen("Your server is offline! Start it in order to manage plugins.")
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
