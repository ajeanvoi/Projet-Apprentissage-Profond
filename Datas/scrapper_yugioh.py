from io import BytesIO
from PIL import Image
from os import path
import requests
import json
import time
import random

def progress(i, vmax):
    D = 20
    if vmax == 1000:
        print(i)
    k = int((D * i) / vmax)
    nk = D - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<< (" + str(i) + "/" + str(vmax) + ")") 

def get_card_list():
    try: #save
        with open("cardlist.json", "rt") as f:
            return json.load(f)["data"]
    except:
        r = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
        time.sleep(0.05)
        with open("cardlist.json", "wt") as f:
            f.write(r.text)
        return r.json()["data"]

def getart(cardinfo, force=bool):
    p = "data/" + str(cardinfo["id"]) + '.jpg'
    if path.exists(p) and path.getsize(p) > 25_000 and not force: # and not force
        return True
    response = requests.get(cardinfo["card_images"][0]["image_url_cropped"])
    time.sleep(0.1)
    if response.status_code != 200:
        #raise Exception('Failed to find the corresponding image of card ' + str(cardinfo["id"]) + ")")
        return True
    img = Image.open(BytesIO(response.content))
    img.save(p)
    return True
def picknarts(d, n, force = False, n_start = 0):
    random.seed("trans rights")
    print("Downloading card art...")
    print()
    j = 0
    z = len(d)
    for i in random.sample(range(0,z), n):
        j += 1
        if j >= n_start:
            progress((j-n_start), (n-n_start))
            if not getart(d[i], force):
                print("FUCK")
                return
    progress((j-n_start), (n-n_start))


cl = get_card_list()
picknarts(cl, 6341)