import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif(fn):
    output = {}
    img = Image.open(fn)
    info = img._getexif()

    if info is None:
        return output

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        output[decoded] = value
    return output


path = 'TODO'
os.chdir(path)

files = []
files += glob.glob("IMG_20160116_000001.jpeg")
# files += glob.glob("*.jpg")
# files += glob.glob("*.jpeg")

for file in files:
    print(file)

    # WARNING: This can return an empty dict, and not all keys exist on all photos
    exif = get_exif(file)

    time = datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")

    print time
    print exif

    # time = time.replace(":", "")
    # time = time.replace(" ", "_")
    # number = 0
    # new_name = time+"_additional_information.jpg"
    # if new_name == file:
    #     print(new_name, "already ok")
    #     continue
    # while os.path.exists(new_name):
    #     number += 1
    #     new_name = time+"_"+str(number)+"_additional_information.jpg"
    # os.rename(file, new_name)
