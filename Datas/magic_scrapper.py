from io import BytesIO
from PIL import Image
import json
import requests
import time
import random
from os import path

def progress(i, vmax):
    D = 20
    if vmax == 1000:
        print(i)
    k = int((D * i) / vmax)
    nk = D - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<< (" + str(i) + "/" + str(vmax) + ")") 

def tstrip(s: str):
    return s[0:4] + s[5:7] + s[8:10] + s[11:13] + s[14:16] + s[17:19]
def rget(l: str, n: str, a: bool):
    #makes GET request and waits to add the requested artificial delay
    #returns them as JSON
    #saves them to avoid duplicating requests.
    if not a: #nosave
        r = requests.get(l)
        time.sleep(0.05)
        return r.json()
    try: #save
        with open(n + ".json", "rt") as f:
            return json.load(f)
    except:
        r = requests.get(l)
        time.sleep(0.05)
        with open(n + ".json", "wt") as f:
            f.write(r.text)
        return r.json()


def getbulklist():
    return rget("bulk-data", False)

def getlist():
    #grabs the filtered art card list
    m = True
    i = 1
    j = 0
    l = "https://api.scryfall.com/cards/search?q=legal%3Acommander+-t%3Aland+is%3Abooster+layout%3Anormal&order=released&as=grid&unique=art"
    d = []
    print("Getting card list...")
    print()
    while m:
        b = rget(l, "card-list-" + str(i), True)
        vmax = b["total_cards"]
        j += len(b["data"])
        progress(j, vmax)
        i += 1
        if b["has_more"]:
            l = b["next_page"]
        else: m = False
        d.extend(b["data"])
    return d

def getart(cardinfo, force=bool):
    try:
        p = "data/" + cardinfo["set"] + '_' + cardinfo["collector_number"] + '.jpg'
        if not path.exists(p) or path.getsize(p) > 25_000: # and not force
            return True
        response = requests.get(cardinfo["image_uris"]["art_crop"])
        time.sleep(0.05)
        if response.status_code != 200:
            raise Exception('Failed to find the corresponding image of "' + cardinfo["name"] + " (" + cardinfo["set"] + ")")
        img = Image.open(BytesIO(response.content))
        img.save(p)
        return True
    except:
        return False

def picknarts(d,n,force,n_start=0):
    random.seed("trans rights")
    print("Downloading card art...")
    print()
    j = 0
    for i in random.sample(range(0,len(d)), n):
        j += 1
        if j >= n_start:
            progress((j-n_start), (n-n_start))
            if not getart(d[i], force):
                print("FUCK")
                return
    progress((j-n_start), (n-n_start))


b = getlist()
picknarts(b, 1650, True)


# b = getbulklist()

# j = {}
# for it in b["data"]:
# if it["type"] == "unique_artwork":
# j = it
# break

# d = rget("unique-artwork")

#print("Retrieving element list")
#data = json.load(open("unique-artwork.json", "r"))
#print(len(data))