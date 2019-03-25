import requests
import discord
import json
import cv2
import os

import error
import files

keys = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

def view(f, server=True, args=""):
    r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/server_data", headers={"Authorization" : f["auth"]}).text)
    name = r["server"]["name"]

    if server == True:
        motd = r["server"]["motd"]
    else:
        motd = ""
        for i in args:
            motd += i + " "

    motd = motd.replace(" ", "%20")

    if "&" in motd:
        motdSplit = motd.split("&")
        for i in motdSplit:
            if i != "":
                key = i[0]
                if key in keys:
                    motd = motd.replace("&" + key, "<<" + key + ">>")

    r = requests.get("https://render-tron.appspot.com/screenshot/http://rpiweb.000webhostapp.com/motd.php%3Fname%3D" + name + "%26motd%3D" + motd, stream=True)
    if r.status_code == 200:
        with open("./motds/" + name + ".png", 'wb') as file:
            for chunk in r:
                file.write(chunk)
        img = cv2.imread("./motds/" + name + ".png")
        img = img[10:130, 10:1000]
        cv2.imwrite("./motds/" + name + ".png", img)

    file = discord.File("./motds/" + name + ".png", "motd.png")
    os.remove("./motds/" + name + ".png")
    return file
