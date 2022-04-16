import os
import subprocess
import glob
from PIL import Image

import sys

##########################################
ini = open("novel.ini")
magick_convert = ini.readline().replace("MAGICK_CONVERT_PATH ", "").replace("\n", "")
bg_width = int(ini.readline().replace("BG_WIDTH ", ""))
bg_height = int(ini.readline().replace("BG_HEIGHT ", ""))
bg_top = int(ini.readline().replace("BG_TOP ", ""))
text_top = int(ini.readline().replace("TEXT_TOP ", ""))
text_bottom = int(ini.readline().replace("TEXT_BOTTOM ", ""))
text_left = int(ini.readline().replace("TEXT_LEFT ", ""))
text_right = int(ini.readline().replace("TEXT_RIGHT ", ""))
compression = ini.readline().replace("COMPRESSION ", "").replace("\n", "")

tmp_back =  glob.glob('novel\\background\\**\\*.png', recursive=True)
if (len(tmp_back) == 0):
    tmp_back =  glob.glob('novel\\background\\**\\*.jpg', recursive=True)
if (len(tmp_back) == 0):
    print("The project does not have backgrounds.")
    print("This way even the foregrounds will be ignored")
    exit()

tmp_back = tmp_back[0]
tmp_back = Image.open(tmp_back)
img_scale = (bg_width * 8) / tmp_back.size[0]

bg_left = int((40 - bg_width) / 2)

#############################################

bg_width *= 8
bg_height *= 8

if not os.path.exists('res'):
    os.mkdir('res')

if not os.path.exists('res/background'):
    os.mkdir('res/background')
for d in glob.glob("novel\\background\\**\\*\\", recursive = True):
    d = d.replace("novel", "res", 1)
    if not os.path.exists(d):
        os.mkdir(d)

if not os.path.exists('res/foreground'):
    os.mkdir('res/foreground')
for d in glob.glob("novel\\foreground\\**\\*\\", recursive = True):
    d = d.replace("novel", "res", 1)
    if not os.path.exists(d):
        os.mkdir(d)


if not os.path.exists('res/script'):
    os.mkdir('res/script')
for d in glob.glob("novel\\script\\**\\*\\", recursive = True):
    d = d.replace("novel", "res", 1)
    if not os.path.exists(d):
        os.mkdir(d)

def scale_n_save_bg(image_file):
    img = Image.open(image_file)
    scaled = img.resize([bg_width, bg_height])
    scaled.save(image_file)

def scale_n_save_fg(image_file):
    img = Image.open(image_file)
    scaled = img.resize([int(img.size[0] * img_scale), int(img.size[1] * img_scale)])
    scaled.save(image_file)


def crop_n_save(image_file):
    img = Image.open(image_file)
    # 8 + 1 cause this way we will not cut the images
    x = int(img.size[0] / 8 + 1) * 8 - 4 #this is -4 so to cut both sides
    y = int(img.size[1] / 8 + 1) * 8 #this is 8 + 1 to make the image taller and not cut it.
    dif = img.size[1] - y
    cropped = img.crop((4,dif,x,y + dif))
    cropped.save(image_file)
    #cropped.convert('P').convert('P', palette=Image.ADAPTIVE, colors=16).save(image_file)
    #-fx -1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u -ordered-dither o8x8,8 -colors 16 -ordered-dither threshold,8,8,8

if len(sys.argv) > 1:
    d = False
    if "background" in sys.argv[1]:
        d = False
    elif "foreground" in sys.argv[1]:
        d = True
    else:
        print("argument does not belong to an image")
        exit()
    out = sys.argv[1].replace('novel\\', 'res\\').replace('.jpg', '.png').lower()
    subprocess.run([magick_convert,
    sys.argv[1], 
    '-fx',
    '-1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u',
    '-ordered-dither',
    'o8x8,8',
    '-colors',
    '16',
    '-ordered-dither',
    'threshold,8,8,8',
    out])
    if d:
        if(img_scale != 1.0):
            scale_n_save_fg(out)
        crop_n_save(out)
    else:
        if(img_scale != 1.0):
            scale_n_save_bg(out)
    exit()

def convert_images():
    for background in glob.glob('novel\\background\\**\\*.jpg', recursive=True):
        out = background.replace('novel\\', 'res\\').replace('.jpg', '.png').replace("-", "_").lower()
        subprocess.run([magick_convert,
        background, 
        '-fx',
        '-1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u',
        '-ordered-dither',
        'o8x8,8',
        '-colors',
        '16',
        '-ordered-dither',
        'threshold,8,8,8',
        out])

        print(out)
        if(img_scale != 1.0):
            scale_n_save_bg(out)

    for background in glob.glob('novel\\background\\**\\*.png', recursive=True):
        out = background.replace('novel\\', 'res\\').lower().replace("-", "_")
        subprocess.run([magick_convert,
        background, 
        '-fx',
        '-1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u',
        '-ordered-dither',
        'o8x8,8',
        '-colors',
        '16',
        '-ordered-dither',
        'threshold,8,8,8',
        out])

        print(out)
        if(img_scale != 1.0):
            scale_n_save_bg(out)

    for foreground in glob.glob('novel\\foreground\\**\\*.png', recursive=True):
        out = foreground.replace('novel\\', 'res\\').lower().replace("-", "_")
        subprocess.run([magick_convert,
        foreground, 
        '-fx',
        '-1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u',
        '-ordered-dither',
        'o8x8,8',
        '-colors',
        '16',
        '-ordered-dither',
        'threshold,8,8,8',
        out])

        print(out)
        if(img_scale != 1.0):
            scale_n_save_fg(out)
        crop_n_save(out)

convert_images()


