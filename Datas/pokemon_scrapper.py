from PIL import Image
import os
import time
import requests
import json
from io import BytesIO

#api key
api_key = "59f4e759-7ba3-4742-a247-f911075742b9"

def progress(i, vmax):
    D = 20
    if vmax == 1000:
        print(i)
    k = int((D * i) / vmax)
    nk = D - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<< (" + str(i) + "/" + str(vmax) + ")") 

# Recoupage des images
def crop(image, ed, factor):
    box = {
        'sv4pt5': (132, 117, 673, 482),
        'bw4': (143, 119, 666, 502), 
        'base1': (177, 135, 644, 478),
        'ex8': (66, 104, 668, 444),
        'dp6': (162, 139, 665, 470),
        'pl4': (150, 134, 668, 510),
        'hgss2': (58, 132, 676, 500),
        'bw11': (147, 124, 670, 505),
        'swsh11tg': (120, 125, 672, 480),
        'sv3': (135, 119, 672, 483),
        'base2': (165, 165, 640, 469),
        'base3': (165, 165, 640, 469),
        'sv3pt5': (139, 124, 672, 480),

        'sm9': (129, 129, 673, 482),
        'sm10': (125, 125, 678, 470),
        'swsh12pt5': (122, 127, 675, 480),
        'sv5': (140, 124, 670, 478),
        'bw7': (148, 120, 665, 495),
    }
    if not ed in box.keys():
        return image
    cropped_image = image.crop((round(box[ed][0] * factor), round(box[ed][1] * factor), round(box[ed][2] * factor), round(box[ed][3] * factor)))
    return cropped_image
def recrop():
    box = {
        'bw7': (90, 73, 407, 300),
    }
    f = 1.65
    for k in box.keys():
        print("'" + k + "':", "(" + str(round(box[k][0] * f)) + ",", str(round(box[k][1] * f)) + ",", str(round(box[k][2] * 1.65)) + ",", str(round(box[k][3] * 1.65)) + "),")

def url_pcd(ed, n):
    return 'https://www.pokecardex.com/assets/images/sets/' + ed + '/HD/' + str(n) + '.jpg'
def url_pk(ed, n):
    return 'https://www.pokemon.com/static-assets/content-assets/cms2/img/cards/web/' + ed + '/' + ed + '_EN_' + str(n) + '.png'

def load_sets():
    try: 
        with open("sets.json", "rt") as f:
            return json.load(f)
    except:
        cd = requests.get("https://api.pokemontcg.io/v2/sets", headers={"X-Api-Key":api_key})
        with open("sets.json", "wt") as f:
                f.write(cd.text)
        return cd.json()
def load_set(ed):
    try: 
        with open("sets/" + ed + ".json", "rt") as f:
            return json.load(f)["data"]
    except:
        cd = requests.get('https://api.pokemontcg.io/v2/cards?q=set.id:' + ed + ' supertype:Pokémon', headers={"X-Api-Key":api_key})
        with open("sets/" + ed + ".json", "wt") as f:
                f.write(cd.text)
        return cd.json()["data"]

def get_cards(ed, test):
    d = load_set(ed)
    print()
    vmax = 10 if test else len(d)
    for i in range(vmax):
        try:
            response = requests.get(d[i]["images"]["large"], headers={"X-Api-Key":api_key})
            if response.status_code != 200:
                raise Exception('Failed to find the corresponding image of url ' + d[i].images.large)
            time.sleep(0.05)
            img = Image.open(BytesIO(response.content))
            cimg = crop(img, ed, (img.size[1] / 1024))
            cimg.save("data/" + d[i]["id"] + '.png')
            progress(i+1, vmax)
        except Exception as e:
            print("Erreur réseau!")
            print(e)
            return e




#load_sets()
recrop() # 76, 67, 411, 285
get_cards('bw7', False)

