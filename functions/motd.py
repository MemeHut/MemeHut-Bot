import requests
import discord
import json

import error
import files

def view(guild, server=True):
    f = files.read("../Bot-Storage/" + guild + ".json", True)
 
    if f == "FileNotFoundError":
        return error.gen("You have not setup your server yet!")
    elif f == "JSONDecodeError":
        return error.gen("Your server's file seems to be corrupted, please contact us or reset your server. \n\n!contact \n!reset")
    
    r = requests
