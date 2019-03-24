import requests
import discord
import json

import error
import files

def view(guild, server=True):
    f = files.read()
