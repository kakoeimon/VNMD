import os
from sre_parse import FLAGS
import subprocess
import glob
from PIL import Image
import PIL
import sys

from numpy import append

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

if os.path.isfile(magick_convert):
    print("Using ImageMagick")
else:
    print("Using ony PILLOW")
    magick_convert = False
#############################################

bg_width *= 8
bg_height *= 8

alpha_color = [255, 0, 255]

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
    if img.size[1] % 8 == 0:
        cropped = img.crop((4,0,x,y))
    else:
        dif = img.size[1] - y
        cropped = img.crop((4,dif,x,y + dif))
    cropped.save(image_file)

def reduce_colors_convert(img_file, num_colors):
    subprocess.run([magick_convert,
        img_file, 
        '-fx',
        '-1.28500726818617*u*u*u + 1.92751090227925*u*u + 0.357496365906917*u',
        '-ordered-dither',
        'o8x8,8',
        '-colors',
        str(num_colors),
        '-ordered-dither',
        'threshold,8,8,8',
        img_file])

    img = Image.open(img_file)
    if img.mode != "P":
        img = img.convert("RGB").quantize(num_colors)
        img.save(img_file)

def replace_alpha(img_file):
    if magick_convert == False:

        img = Image.open(img_file)
        bg = Image.new("RGB", img.size, (0, 0, 0)).convert("L")
        pink = Image.new("RGBA", img.size, (alpha_color[0], alpha_color[1], alpha_color[2]))
        bg = Image.composite(pink, img, bg)
        bg.save(img_file)
    else:
        img = Image.open(img_file)
        alpha = img.getchannel('A')
        bg = Image.new(img.mode, img.size, (0, 0, 0, 255))
        bg.paste(alpha, mask=alpha)
        bg = bg.quantize(2).convert("L")
        pink = Image.new("RGBA", img.size, (alpha_color[0], alpha_color[1], alpha_color[2]))
        bg = Image.composite(img.convert("RGB"), pink, bg)
        bg.save(img_file)


def check_colors(img_file: str):
    original_img = Image.open(img_file)
        #pal = Image.open("Mega_Drive_Palette_indexed.png")
    img = original_img.convert(mode="RGB")
    #print(len(img.getcolors()))
    if magick_convert == False:
        
        if "background" in img_file:
            img = original_img.quantize(16, dither=0)
            pal = img.getpalette()
            
            if (len(pal)) >= 16*3:
                black_index = -1
                pal = img.getpalette()
                for i in range(0, 16):
                    if pal[i*3] == 0 and pal[i*3 + 1] == 0 and pal[i*3 + 2] == 0:
                        black_index = i
                        break
                if black_index > 0 and black_index < 16:
                    remap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                    remap[0] = black_index
                    remap[black_index] = 0
                    img = img.remap_palette(remap)
                else:
                    img = original_img.quantize(15, dither=0)
            if len(img.getcolors()) < 16:
                pal = img.getpalette()
                while len(pal) < 16*3:
                    pal.append(0)
                    pal.append(0)
                    pal.append(0)

                pal[15*3] = 0
                pal[15*3+1] = 0
                pal[15*3+2] = 0
                img.putpalette(pal)
                img = img.remap_palette([15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0])

                
        elif "foreground" in img_file:
            img = original_img.quantize(15, dither=0)
            pal = img.getpalette()
            while len(pal) < 16 * 3:
                pal.append(0)
                pal.append(0)
                pal.append(0)
            pal[15*3] = 255
            pal[15*3 + 1] = 255
            pal[15*3 + 2] = 255
            img.putpalette(pal)
            
        img.save(img_file)
    else: #MAGICK CONVERT
        img = original_img.convert("RGB")
        if "background" in img_file:
            img.close()
            reduce_colors_convert(img_file, 16)
            img = Image.open(img_file)
            pal = img.getpalette()
            
            if (len(pal)) >= 16*3:
                black_index = -1
                pal = img.getpalette()
                for i in range(0, 16):
                    if pal[i*3] == 0 and pal[i*3 + 1] == 0 and pal[i*3 + 2] == 0:
                        black_index = i
                        break
                if black_index > 0 and black_index < 16:
                    remap = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                    remap[0] = black_index
                    remap[black_index] = 0
                    img = img.remap_palette(remap)
                else:
                    original_img.save(img_file)
                    img = Image.open(img_file)
                    reduce_colors_convert(img_file, 15)
                    img = Image.open(img_file)
            if len(img.getcolors()) < 16:
                pal = img.getpalette()
                while len(pal) < 16*3:
                    pal.append(0)
                    pal.append(0)
                    pal.append(0)

                pal[15*3] = 0
                pal[15*3+1] = 0
                pal[15*3+2] = 0
                img.putpalette(pal)
                img = img.remap_palette([15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0])

                
        elif "foreground" in img_file:
            reduce_colors_convert(img_file, 15)
            img = Image.open(img_file)
            pal = img.getpalette()
            while len(pal) < 16 * 3:
                pal.append(0)
                pal.append(0)
                pal.append(0)
            pal[15*3] = 255
            pal[15*3 + 1] = 255
            pal[15*3 + 2] = 255
            img.putpalette(pal)
            
        img.save(img_file)
    
    
def check_back_size(img_file):
    img = Image.open(img_file)
    crop = img.crop((0,0, bg_width, bg_height))
    crop.save(img_file)



def convert_images():
        
    for background in glob.glob('novel\\background\\**\\*.jpg', recursive=True):
        out = background.replace('novel\\', 'res\\').replace('.jpg', '.png').replace("-", "_").replace("~", "_").lower()
        print(out)
        img = Image.open(background).convert("RGBA")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        check_back_size(out)
        check_colors(out)

    for background in glob.glob('novel\\background\\**\\*.png', recursive=True):
        out = background.replace('novel\\', 'res\\').lower().replace("-", "_").replace("~", "_")
        print(out)
        img = Image.open(background).convert("RGB")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        check_back_size(out)
        check_colors(out)
    
    for foreground in glob.glob('novel\\foreground\\**\\*.png', recursive=True):
        out = foreground.replace('novel\\', 'res\\').lower().replace("-", "_").replace("~", "_")
        
        img = Image.open(foreground).convert("RGBA")
        img.save(out)
        print(out)
        if(img_scale != 1.0):
            scale_n_save_bg(out)
        crop_n_save(out)
        replace_alpha(out)
        check_colors(out)

    




        


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
    
    img = Image.open(sys.argv[1]).convert("RGB")
    img.save(out)

    if(img_scale != 1.0):
        scale_n_save_bg(out)
    if d:
        img = Image.open(sys.argv[1]).convert("RGBA")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        crop_n_save(out)
        replace_alpha(out)
        check_colors(out)
    else:
        img = Image.open(sys.argv[1]).convert("RGB")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        check_back_size(out)
        check_colors(out)
    print(out)

else:
    convert_images()


