from io import BytesIO
from PIL import Image
import json
import requests
import time
import random
import os

def progress(i, vmax):
    D = 20
    if vmax == 1000:
        print(i)
    k = int((D * i) / vmax)
    nk = D - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<< (" + str(i) + "/" + str(vmax) + ")") 


def new_formatter(height: int, aspect_ratio: float, quality: int, stretch: bool):
    width = int(aspect_ratio * height)
    if quality > 100: 
        print("Quality should be <= 1")
        return None
    def format(dir: str, img: str):
        i = Image.open(dir + "/" + img)
        os.remove(dir + "/" + img)
        [img, _] = img.split(".", 1)
        if i.size[0] < width or i.size[1] < height:
            raise ValueError('Invalid size: image ' + dir + "/" + img + " too small")
        # downsize the image with an ANTIALIAS filter (gives the highest quality)
        i = i.resize((width,height),Image.LANCZOS)
        i = i.convert("RGB")
        if quality < 100:
            i.save(dir + "/" + img + '.jpg', optimize=True, quality=quality)
        else:
            i.save(dir + "/" + img + '.png')
    return format


def processall(dir: str, fun):
    ld = os.listdir(dir)
    k = []
    for l in ld:
        if l.endswith(".png") or l.endswith(".jpg"):
            k.append(l)
    ld = k
    print("Formatting images:\n")
    for i in range(len(ld)):
        f = ld[i]
        progress(i, len(ld))
        try:
            fun(dir, f)
        except:
            raise ValueError("Failed formatting for image " + f)
    progress(len(ld), len(ld))

processall("../yugiyo", new_formatter(128, 1, 95, True))