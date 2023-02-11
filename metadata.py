import os
import subprocess

import hachoir

from PIL import Image, ExifTags
from PIL.TiffTags import TAGS

# from PIL.ExifTags import TAGS


def get_meta(picture):
    with Image.open(picture) as img:
        print(img.tag.keys())
        meta_dict = {TAGS[key]: img.tag[key] for key in img.tag.keys()}

    return meta_dict


# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

for f in os.listdir("data"):
    if not f.endswith(("ff", "jpeg")):
        print("Ignore")
        continue
    image_path = f"data/{f}"
    image = Image.open(image_path)
    if f.endswith("ff"):
        d = get_meta(image_path)
        print(d)
        exif_data = image.getexif()
        # iterating over all EXIF data fields
        exif_data = {
            ExifTags.TAGS[k]: v
            for k, v in image.getexif().items()
            if k in ExifTags.TAGS
        }
        exif_data = image._getexif()

    elif f.endswith("jpeg"):

        exeProcess = "hachoir-metadata"
        process = subprocess.Popen(
            [exeProcess, image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        infoDict = {}
        for tag in process.stdout:
            line = tag.strip().split(":")
            infoDict[line[0].strip()] = line[-1].strip()

        for k, v in infoDict.items():
            t = print(k, ":", v)
