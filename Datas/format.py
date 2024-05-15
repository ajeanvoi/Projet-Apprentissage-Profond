#! /usr/local/bin/python3
from PIL import Image
import os
import sys

def progress(i, vmax):
    D = 20
    if vmax == 1000:
        print(i)
    k = int((D * i) / vmax)
    nk = D - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<< (" + str(i) + "/" + str(vmax) + ")") 


def new_formatter(height: int, aspect_ratio: float, quality: int, stretch: bool):
    width = int(aspect_ratio * height)
    print("Image properties: ")
    print("    Size:", str(height) + "x" + str(width), "(ar=" + str(aspect_ratio) + ")")
    print("    Quality:", str(quality) + "%")
    if quality > 100: 
        print("Quality should be <= 100%")
        return None
    def format(dir: str, img: str):
        i = Image.open(dir + "/" + img)
        [img, ox] = img.split(".", 1)
        if i.size[0] < width or i.size[1] < height:
            raise ValueError('Invalid size: image ' + dir + "/" + img + " too small")
        # downsize the image with an ANTIALIAS filter (gives the highest quality)
        i = i.resize((width,height),Image.LANCZOS)
        i = i.convert("RGB")
        if quality < 100:
            try:
                i.save(dir + "/" + img + '.jpg', optimize=True, quality=quality)
            except:
                raise ValueError("HLFIQGD")
            if "jpg" != ox: 
                os.remove(dir + "/" + img + "." + ox)
        else:
            i.save(dir + "/" + img + '.png')
            if "png" != ox: 
                os.remove(dir + "/" + img + "." + ox)
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
            #os.remove(dir + "/" + f)
        except:
            raise ValueError("Failed formatting for image " + f)
    progress(len(ld), len(ld))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: format <folder> <size> <aspect_ratio> <quality>")
    else: processall(sys.argv[1], new_formatter(int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), True))