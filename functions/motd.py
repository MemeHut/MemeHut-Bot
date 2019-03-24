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
    
   r = json.loads(requests.get("https://api.minehut.com/server/" + f["servers"][f["server"]] + "/server_data", headers={"Authorization" : f["auth"]}).text)
    name = r["name"]
    motd = r["motd"]

    motd = motd.replace("&0", "<<0>>")
    motd = motd.replace("&1", "<<1>>")
    motd = motd.replace("&2", "<<2>>")
    motd = motd.replace("&3", "<<3>>")
    motd = motd.replace("&4", "<<4>>")
    motd = motd.replace("&5", "<<5>>")
    motd = motd.replace("&6", "<<6>>")
    motd = motd.replace("&7", "<<7>>")
    motd = motd.replace("&8", "<<8>>")
    motd = motd.replace("&9", "<<9>>")
    motd = motd.replace("&a", "<<a>>")
    motd = motd.replace("&b", "<<b>>")
    motd = motd.replace("&c", "<<c>>")
    motd = motd.replace("&d", "<<d>>")
    motd = motd.replace("&e", "<<e>>")
    motd = motd.replace("&f", "<<f>>")

    r = requests.get("https://render-tron.appspot.com/screenshot/http://rpiweb.000webhostapp.com/motd.php%3Fname%3D" + name + "%26motd%3D" + motd, stream=True)
    if r.status_code == 200:
        with open("motd.png", 'wb') as file:
            for chunk in r:
                file.write(chunk)
        img = cv2.imread("motd.png")
        img = img[10:130, 10:1000]
        cv2.imwrite("motd.png", img)
    
