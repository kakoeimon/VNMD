from PIL import Image
import glob
import shutil
import os

if os.path.exists('out'):
    shutil.rmtree("out")

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


novel_res = open('res/novel_images_res.res', 'w')
images_h = open('inc/novel_images.h', 'w')
images_c = open('src/novel_images.c', 'w')

images_h.write("#ifndef H_NOVEL_IMAGES\n")
images_h.write("#define H_NOVEL_IMAGES\n\n")
images_h.write("#include \"genesis.h\"\n")
images_h.write("#include \"novel_images_res.h\"\n\n")

images_h.write("#define NOVEL_TEXT_TOP " + str(text_top) + "\n")
images_h.write("#define NOVEL_TEXT_BOTTOM " + str(text_bottom) + "\n")
images_h.write("#define NOVEL_TEXT_LEFT " + str(text_left) + "\n")
images_h.write("#define NOVEL_TEXT_RIGHT " + str(text_right) + "\n")
images_h.write("#define NOVEL_TEXT_WIDTH " + str(text_right - text_left) + "\n\n")

images_h.write("#define NOVEL_BG_WIDTH " + str(bg_width) + "\n")
images_h.write("#define NOVEL_BG_HEIGHT " + str(bg_height) + "\n")
images_h.write("#define NOVEL_BG_TOP " + str(bg_top) + "\n")
images_h.write("#define NOVEL_BG_LEFT " + str(int(bg_left)) + "\n\n")


images_h.write("extern const Image *NOVEL_BACKGROUND[];\n")
images_h.write("extern const Image *NOVEL_FOREGROUND[];\n")
images_h.write("extern const int NOVEL_FOREGROUND_SIZE[][2];\n")

images_h.write("\n#endif")


images_c.write("#include \"novel_images.h\"\n\n")
images_c.write("const Image *NOVEL_BACKGROUND[] = {\n")


for background in glob.glob('novel\\background\\**\\*.jpg', recursive=True):
    _id = background.replace('novel\\', "").replace('\\', '_').replace(".jpg", "").replace("-", "_").lower()
    novel_res.write("IMAGE " + _id + " " + background.replace('novel\\', "").replace(".jpg", ".png").replace("-", "_") + " " + compression + "\n")
    images_c.write("\t&" + _id + ",\n")
for background in glob.glob('novel\\background\\**\\*.png', recursive=True):
    _id = background.replace('novel\\', "").replace('\\', '_').replace(".png", "").replace("-", "_").lower()
    novel_res.write("IMAGE " + _id + " " + background.replace('novel\\', "").replace("-", "_") + " " + compression + "\n")
    images_c.write("\t&" + _id + ",\n")
images_c.write("};\n\n")

#for background in glob.glob('res\\background\\**\\*.png', recursive=True):
#    _id = background.replace('res\\', "").replace('\\', '_').replace(".png", "")
#    novel_res.write("IMAGE " + _id + " " + background.replace('res\\', "") + " " + compression + "\n")
#    images_c.write("\t&" + _id + ",\n")
#images_c.write("};\n\n")


images_c.write("const Image *NOVEL_FOREGROUND[] = {\n")
foreground_size = []
for foreground in glob.glob('res\\foreground\\**\\*.png', recursive=True):
    _id = foreground.replace('res\\', "").replace('\\', '_').replace(".png", "")
    novel_res.write("IMAGE " + _id + " " + foreground.replace('res\\', "") + " " + compression + "\n")
    images_c.write("\t&" + _id + ",\n")
    foreground_size.append(Image.open(foreground).size)
images_c.write("};\n\n")

images_c.write("const int NOVEL_FOREGROUND_SIZE[][2] = {\n")
for size in foreground_size:
    images_c.write("\t{" + str(int(size[0] / 8)) + ", " + str(int(size[1] / 8)) + "},\n",)
images_c.write("};\n\n")
novel_res.close()
