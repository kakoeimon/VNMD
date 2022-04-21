import os
from sre_parse import FLAGS
import subprocess
import glob
from PIL import Image
import PIL
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

def replace_alpha(img_file):

    img = Image.open(img_file)
    alpha = img.split()[-1]
    bg = Image.new(img.mode, img.size, (0, 0, 0, 255))
    bg.paste(alpha, mask=alpha)
    bg = bg.quantize(2).convert("L")
    pink = Image.new("RGB", img.size, (alpha_color[0], alpha_color[1], alpha_color[2]))
    bg = Image.composite(img.convert("RGB"), pink, bg)
    bg.save(img_file)
    #bg.save(img_file)
    #new_image = Image.new("RGBA", img.size, (255, 0, 255))
    #new_image.paste(img, (0, 0), img)
    #new_image = new_image.convert("RGB")
    #new_image.save(img_file)

def check_colors(img_file: str):
    
    #print(len(img.getcolors()))
    if magick_convert == False:
        img = Image.open(img_file)
        #pal = Image.open("Mega_Drive_Palette_indexed.png")
        img = img.convert(mode="RGB", colors= 256, dither=0)
        #img = img.quantize(256, dither=3, palette=pal)
        #pal = img.quantize(16, method=1)
        #img = img.quantize(16, dither=3, palette=pal, method=1)
        
        if "foreground" in img_file:
            img = img.quantize(16)
            index = 15
            palette = img.getpalette()
            for i in range(0,len(img.getcolors())):
                if palette[i*3] == alpha_color[0] and palette[i*3+1] == alpha_color[1] and palette[i*3+2] == alpha_color[2]:
                    index = i
                    break
            palette = [index]
            for i in range(1,len(img.getcolors())):
                if i == index:
                    palette.append(0)
                else:
                    palette.append(i)
            
            img = img.remap_palette(palette)
        if "background" in img_file:
            bg = img.quantize(14)
            pal = bg.getpalette()
            pal.insert(0, 0)
            pal.insert(0, 0)
            pal.insert(0, 0)
            pal.pop()
            pal.pop()
            pal.pop()

            bg = Image.new("P", [16,16])
            bg.putpalette(pal)
            img = img.quantize(15, palette=bg, dither=0)
            #print(pal)
            
        img.save(img_file)
    else:
        num_colors = 16
        if "background" in img_file:
            num_colors = 14


        reduce_colors_convert(img_file, num_colors)
        img = Image.open(img_file)
        
        
        if img.mode != "P":
            img = img.convert("RGB")
            img = img.quantize(num_colors)
        
        if "background" in img_file:
            bg = img.quantize(14)
            pal = bg.getpalette()
            pal.insert(0, 0)
            pal.insert(0, 0)
            pal.insert(0, 0)
            pal.pop()
            pal.pop()
            pal.pop()
            pal.insert(15*3, alpha_color[0])
            pal.insert(15*3 + 1, alpha_color[1])
            pal.insert(15*3 + 2, alpha_color[2])
            pal.pop()
            pal.pop()
            pal.pop()

            bg = Image.new("P", [16,16])
            bg.putpalette(pal)
            img = img.convert("RGB").quantize(16, palette=bg, dither=0)
        img.save(img_file)
    
    
    
def check_back_size(img_file):
    img = Image.open(img_file)
    crop = img.crop((0,0, bg_width, bg_height))
    crop.save(img_file)



def convert_images():

    for background in glob.glob('novel\\background\\**\\*.jpg', recursive=True):
        out = background.replace('novel\\', 'res\\').replace('.jpg', '.png').replace("-", "_").replace("~", "_").lower()
        
        img = Image.open(background).convert("RGBA")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        check_back_size(out)
        check_colors(out)

        print(out)
        
        

    for background in glob.glob('novel\\background\\**\\*.png', recursive=True):
        out = background.replace('novel\\', 'res\\').lower().replace("-", "_").replace("~", "_")
        
        img = Image.open(background).convert("RGB")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        check_back_size(out)
        check_colors(out)

        print(out)

    for foreground in glob.glob('novel\\foreground\\**\\*.png', recursive=True):
        out = foreground.replace('novel\\', 'res\\').lower().replace("-", "_").replace("~", "_")
        
        img = Image.open(foreground).convert("RGBA")
        img.save(out)

        if(img_scale != 1.0):
            scale_n_save_bg(out)
        crop_n_save(out)
        replace_alpha(out)
        check_colors(out)

        print(out)


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


