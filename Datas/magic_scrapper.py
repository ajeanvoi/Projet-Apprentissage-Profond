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
def rget(l: str, n: str, a: bool, itm: str):
    #makes GET request and waits to add the requested artificial delay
    #returns them as JSON
    #saves them to avoid duplicating requests.
    if not a: #nosave
        r = requests.get(l)
        time.sleep(0.05)
        with open(itm + "/" + n + ".json", "wt") as f:
            f.write(r.text)
        return r.json()
    try: #save
        with open(itm + "/" + n + ".json", "rt") as f:
            return json.load(f)
    except:
        r = requests.get(l)
        time.sleep(0.05)
        with open(itm + "/" + n + ".json", "wt") as f:
            f.write(r.text)
        return r.json()
def updatecc(n: str, itm: str, w: int):
    try: #save
        with open(itm + "/" + n + ".json", "rwt") as f:
            j = json.load(f)
            j["total_cards"] = w
            json.dump(j, f)
            return True
    except: return False

def getbulklist():
    return rget("bulk-data", False)

def getlist(bl = True, di = 1, dj = 0):
    #grabs the filtered art card list
    m = True
    i = di
    j = dj
    l = "https://api.scryfall.com/cards/search?dir=asc&order=released&q=legal%3Acommander+-t%3Aland+layout%3Anormal+is%3Abooster+-frame%3Afuture+-frame%3Ashowcase+-t%3Aplaneswalker&unique=art"
    d = []
    if di == 1:
        print("Getting card list...")
    else:
        print("Forcing card list reload...")
        l = l + "&page=" + str(i)
    print()
    while m:
        b = rget(l, "card-list-" + str(i), bl, "card_list")
        vmax = b["total_cards"]
        j += len(b["data"])
        progress(j, vmax)
        i += 1
        if b["has_more"]:
            l = b["next_page"]
            d.extend(b["data"])
        elif bl: 
            #force reload of last one to check.
            d.extend(getlist(False, i-1, j - len(b["data"])))
            m = False
        else: 
            m = False
            d.extend(b["data"])
    if di > 1:
        print("Updating card count...\n")
        for i in range(1, di):
            progress(i, di)
            updatecc("card-list-" + str(i), "card_list", vmax)
        progress(di, di)
    return d

def getart(cardinfo, force=bool):
    try:
        p = "data/" + cardinfo["set"] + '_' + cardinfo["collector_number"] + '.jpg'
        if path.exists(p) and path.getsize(p) > 25_000 and not force: # and not force
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

def picknarts_set(d, n, force, n_start=0):
    random.seed("trans rights")
    print("Downloading card art...")
    print()
    j = 0
    z = int(len(d) / 175)
    for k in range(z):
        for i in random.sample(range(0,175), n):
            j += 1
            if j >= n_start:
                progress((j-n_start), ((n * z)-n_start))
                if not getart(d[i + 175 * k], force):
                    print("FUCK")
                    return
    progress((j-n_start), ((n * z)-n_start))
def picknarts(d, n, force, n_start = 0):
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


b = getlist()
# for i in b:
#     if i["name"] == "Harvester of Misery":
#         print("Found")
#         break
picknarts(b, 5000, False)


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