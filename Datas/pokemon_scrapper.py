from PIL import Image
import os
import requests
from io import BytesIO

def counter(ed, test):
    box = {'JU': 64, 'FO': 62, 'OBF': 230, 'MEW': 207}
    if not ed in box.keys():
        return 10 if test else 1000
    return 10 if test else (box[ed] + 1)

def progress(i, ed, test):
    v = counter(ed, test)
    if v == 1000:
        print(i)
    k = int((10 * i) / v)
    nk = 10 - k
    print("\033[A\033[K>>> " + "#" * k + " " * nk + " <<<") 

# Recoupage des images
def crop(image, ed):
    box = {'PAF': (80, 71, 408, 292), 'BS': (107, 82, 390, 290), 'NG': (82, 82, 391, 288), 'DX': (40, 63, 405, 269), 'NXD': (83, 73, 407, 287), 'LA': (98, 84, 403, 285), 'AR': (91, 81, 405, 309), 'UL': (35, 80, 410, 303), 'LTR': (89, 75, 406, 306), 'LOR': (73, 76, 407, 291), 'OBF': (82, 72, 407, 293), 'JU': (100, 100, 388, 284), 'FO': (100, 100, 388, 284), 'MEW': (84, 75, 407, 291)}
    if not ed in box.keys():
        return image
    cropped_image = image.crop(box[ed])
    return cropped_image

def load_set(ed, test):
    dir_url = 'https://www.pokecardex.com/assets/images/sets/'
    part1 = ed
    part3 = '/HD/'
    part5 = '.jpg'
    j = counter(ed, test)
    print()
    for i in range(1,j):
        part2 = str(i)
        url = dir_url + part1 +  part3 + part2 + part5
        progress(i, ed, test)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception('Failed to find the corresponding image of url ' + url)
            img = Image.open(BytesIO(response.content))
            cimg = crop(img, ed)
            cimg.save(part1 + '_' + part2 + '.png')
        except Exception as e:
            if i < j and (j != 1000 or i < 10):
                print("Erreur réseau!")
            else:
                print("Edition scrappée.")
            break
        progress(j, ed, test)


load_set('MEW', False)

