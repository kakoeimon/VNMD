import os
import glob
from turtle import right
from PIL import Image
import unicodedata

lines_count = 0

novel_stop_music = 1600

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
save_check = ini.readline().replace("SAVE_CHECK ", "").replace("\n", "")
sound_drv = ini.readline().replace("SOUND_DRV ", "").replace("\n", "")

dithering = True
try:
    dithering = ini.readline().replace("DITHERING ", "").replace("\n", "").strip()
    print("DITHERING is " + dithering)
    if dithering == "FALSE":
        dithering = False
except:
    pass

bad_filenames = False
try:
    bad_filenames = ini.readline().replace("BAD_FILENAMES ", "").replace("\n", "").strip()
    print("BAD FILENAMES is " + bad_filenames)
    if bad_filenames == "TRUE":
        bad_filenames = True
    else:
        bad_filenames = False
except:
    pass

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

external_funcs = {}
external_funcs_file = open("inc\\novel_external_functions.h", "r")
for func in external_funcs_file.readlines():
    if func[:5] == "void ":
        external_funcs[func[5:].replace("(", "").replace(")", "").replace(";", "").strip()] = len(external_funcs)

print(external_funcs)
sounds_positions = {}

for wav in glob.glob("res\\wav\\**\\*.wav", recursive=True):
    sounds_positions[os.path.splitext(wav.replace("res\\wav\\", "").replace("\\", "/"))[0]] = len(sounds_positions)

music_positions = {}

if sound_drv == "XGM":
    for xgm in glob.glob("res\\music\\**\\*.vgm", recursive=True):
        music_positions[xgm.replace("res\\music\\", "").replace(".vgm", "")] = len(music_positions)
elif sound_drv == "2ADPCM" or sound_drv == "4PCM":
    for wav in glob.glob("res\\music\\**\\*.wav", recursive=True):
        music_positions[wav.replace("res\\music\\", "").replace(".wav", "").lower()] = len(music_positions)

#print(music_positions)
#############################################

backgrounds = {}
for bg_file in glob.glob('res/background/**/*.png', recursive=True):
    backgrounds[bg_file.replace("\\", "/").replace("res/background/", "", 1)] = len(backgrounds)


foregrounds = {}
for fr_file in glob.glob('res/foreground/**/*.png', recursive=True):
    foregrounds[fr_file.replace("\\", "/").replace("res/foreground/", "", 1)] = len(foregrounds)

###############

def count_line(lines, i):
    count = 0
    line = lines[i].lstrip()
    coms = line.split()
    c = line.split(" ")[0].replace("\n", "").replace("\t", "")
    if c == "bgload":
        count += 5
    elif c == "setimg":
        count += 7
    elif c == "sound":
        t = line.replace("sound ", "", 1).replace("\n", "").replace("\t", " ").strip().split(" ")
        t[0] = os.path.splitext(t[0].replace("\\", "/"))[0]
        if t[0] in sounds_positions.keys() or t[0] == "~":
            
            count += 4
        count += 0
    elif c == "music":
        #t = line.replace("music ", "", 1).replace("\n", "").replace("\t", " ").strip().split(" ")
        #if t[0] in music_positions.keys() or t[0] == "~":
        #    count += 2
        count += 3
    elif c == "text":
        t = line.replace("text ", "", 1).replace("\n", "").replace("\t", " ").lstrip()
        if len(t) == 0 or t[0] == "~":
            return 0
        count += len(t) + 2
    elif c == "choice":
        count +=2
        choice = line.replace("choice ", "", 1).replace("\n", "").replace("\t", " ").split("|")
        for c in choice:
            count += len(c.strip()) + 1
    elif c == "ifchoice":
        count +=2
        choice = line.replace("ifchoice ", "", 1).replace("\n", "").replace("\t", " ").split("|")
        for c in choice:
            count +=7
            ifs = c.split(":")
            if len(ifs) == 2:
                c = ifs[1]
            count += len(c.strip()) + 1
    elif c == "setvar" or c == "gsetvar":
        if (coms[1] == "~"):
            count += 1
        else:
            count += 7
    elif c == "gsetvar":
        count += 0
    elif c == "if":
        count += 9
    elif c == "fi":
        count += 1
    elif c == "jump":
        t = line.strip().replace("\t", "").replace("jump ", "", 1).lower().replace("\n", "").replace("/", "_").replace(".scr", "").strip().split(" ")
        key = t[0].replace("-", "_")
        count += 7
    elif c == "delay":
        count += 3
    elif c == "random":
        count += 0
    elif c == "label":
        count += 0
    elif c == "goto":
        count += 5
    elif c == "cleartext":
        count += 0
    else:
        ############### EXTERNAL FUNCTIONS
        func = line.split(" ")[0].strip()
        if func in external_funcs:
            count +=2
    return count


def count_to_fi(lines, i, ifs_count):
    
    line = lines[i].lstrip()
    count = count_line(lines, i)

    c = line.split(" ")[0].replace("\n", "").replace("\t", "")
    if c == "if":
        ifs_count +=1
    elif c == "fi":
        if ifs_count == 0:
            count += 1
            return count
        else:
            ifs_count -=1
    return count + count_to_fi(lines, i+1, ifs_count)

functions = {"bgload":0, "setimg":1, "sound":2, "music":3,
            "text":4, "choice":5, "setvar":6, "gsetvar":7,
            "if":8, "fi":9, "jump":10, "delay":11, "random":12,
            "label":13, "goto": 14, "cleartext": 15 , "reset_vars": 16,
            "retjump": 17, "ifchoice": 18, "external_func": 19,

}

def get_novel_script_alias(script_file):
    f = script_file.replace("res\\", "", 1).replace(".scr", "")
    
    alias = f.replace("\\", "_").replace("-", "_").lower().replace("novel_script_", "", 1).replace("~", "_").replace("\"", "")
    return alias



if not os.path.exists('res/script'):
    os.mkdir('res/script')




scripts_c = open("src\\novel_scripts.c", "w")
scripts_c.write("#include \"novel_scripts.h\"\n\n")
scripts_c.write("const u8* NOVEL_SCRIPTS[] = {\n")
scripts_c.write("\tscript_main,\n")


script_res = open("res\\scripts_res.res", "w")
#script_res.write("NEAR\n")

scripts_dir = {"main":0}
script_label = {"main": {}}
script_var = {"selected":0, "retfile":1, "retlabel":2}
script_retfile = ["retfile"]
script_retlabel = ["retlabel"]
script_byte_count = []
tmp_var = {}
tmp_global_var = {}
for d in glob.glob('novel\\script\\**\\*\\', recursive=True):
    d = d.replace("novel", "res", 1)
    if not os.path.exists(d):
        os.mkdir(d)

for script_file in glob.glob('novel\\script\\**\\*.scr', recursive=True):

    alias = get_novel_script_alias(script_file)
    if alias != "main":
        script_label[alias] = {}
    try:
        utflines = open(script_file, 'r', encoding="UTF8").readlines()
        lines = []
        for i in range(len(utflines)):
            lines.append(unicodedata.normalize('NFKD', utflines[i]).encode('ascii', 'ignore').decode('ascii'))
    except Exception as e:
        print("------------------ ERROR ---------------")
        print("at file " + script_file)
        print(e)
        exit()
    
    bytes_count = 0
    for i in range(len(lines)):
        line = lines[i].lstrip()
        l = line.replace("\t", " ").replace("\n", " ").replace(":", " ").lstrip().split()
        bytes_count += count_line(lines, i)

        
        if len(l) == 0:
            pass
        elif l[0] == "label":
            script_label[alias][l[1].lower()] = bytes_count
        elif l[0] == "gsetvar":
            if l[1].lower() not in tmp_global_var.keys() and l[1].lower() != "selected":
                tmp_global_var[l[1].lower()] = len(tmp_global_var)
        elif l[0] == "setvar":
            l[1] = l[1].lower()
            if l[1] != "~" and l[1] not in tmp_var.keys() and l[1] != "selected":
                l[3] = l[3].lower()                
                tmp_var[l[1]] = len(tmp_var)
                
                
            pass
            pass

tmp_global_var = sorted(tmp_global_var)
tmp_var = sorted(tmp_var)
num_global_var = len(tmp_global_var)

for key in tmp_global_var:
    script_var[key] = len(script_var)
for key in tmp_var:
    script_var[key] = len(script_var)




scripts_h = open("inc\\novel_scripts.h", "w")
scripts_h.write("#ifndef H_NOVEL_SCRIPTS\n")
scripts_h.write("#define H_NOVEL_SCRIPTS\n\n")
scripts_h.write("#include \"genesis.h\"\n")
scripts_h.write("#include \"scripts_res.h\"\n\n")
scripts_h.write("extern const u8* NOVEL_SCRIPTS[];\n\n")
scripts_h.write("extern const s32 NOVEL_SCRIPTS_BYTES_COUNT[];\n\n")
scripts_h.write("\n#endif\n")

#print(script_label)

for script_file in glob.glob('novel\\script\\**\\*.scr', recursive=True):
    f = script_file.replace("res\\", "", 1).replace(".scr", "")
    
    alias = f.replace("\\", "_").replace("novel_script_", "", 1).replace("-", "_").lower()
    
    if alias != "main":
        scripts_dir[alias] = len(scripts_dir)


#print(scripts_dir)

for script_file in glob.glob('novel\\script\\**\\*.scr', recursive=True):
    bytes_count = 0
    script = open(script_file, 'r', encoding="UTF8")
    out_file = script_file.replace("novel\\", "res\\").replace(".scr", ".bin").replace("-", "_")
    #print(out_file)
    out = open(out_file, 'wb')
    utflines = script.readlines()
    lines = []
    for i in range(len(utflines)):
        lines.append(unicodedata.normalize('NFKD', utflines[i]).encode('ascii', 'ignore').decode('ascii'))

    for i in range(len(lines)):
        #lines[i] = lines[i].lstrip()
        line = lines[i].lstrip()
        coms = line.split()
        
        bytes_count += count_line(lines, i)
        c = line.split(" ")[0].replace("\n", "").replace("\t", "")
        if c == "bgload":
            out.write(functions["bgload"].to_bytes(1, "big"))
            t = line.replace("bgload ", "", 1).lower().replace("\\", "/").replace(".jpg", ".png").replace("\n", "").replace("\t", "").split(" ")
            key = t[0]
            if not ".png" in key: key += ".png" #To make it so we do not have to put the extension every time we use it
            try:
                out.write(backgrounds[key].to_bytes(2, "big"))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe background image " + key + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                #print(backgrounds.keys())
                #out.write(backgrounds[backgrounds.keys().0].to_bytes(1, "big"))
                exit()
            if len(t) == 2 and t[1].isnumeric():
                out.write(int(t[1]).to_bytes(2, "big"))
            else:
                out.write((0).to_bytes(2, "big")) #16 in vnds
            
            
        elif c == "setimg":
            out.write(functions["setimg"].to_bytes(1, "big"))
            t = line.replace("setimg ", "", 1).lower().replace("\\", "/").replace(".jpg", ".png").replace("\n", "").replace("\t", "").split(" ")
            key = t[0]
            if not ".png" in key: key += ".png" #To make it so we do not have to put the extension every time we use it
            try:
                out.write(foregrounds[key].to_bytes(2, "big"))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe foreground image \"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                exit()
            if len(t) > 1:
                #x = int((float(t[1]) * img_scale) / 8 + bg_left)
                x = int((float(t[1])) / 8 + bg_left)
                out.write(x.to_bytes(2, "big", signed=True))
            else:
                out.write(int(0).to_bytes(2, "big", signed=True))
            if len(t) > 2:
                #y = int((float(t[2]) * img_scale) / 8 + bg_top)
                y = int((float(t[2])) / 8 + bg_top)
                out.write(y.to_bytes(2, "big", signed=True))
            else:
                out.write(int(0).to_bytes(2, "big", signed=True))
        elif c == "sound":
            t = line.replace("sound ", "", 1).replace("\n", "").replace("\t", " ").strip().split(" ")
            t[0] = os.path.splitext(t[0].replace("\\", "/"))[0]
            if t[0] in sounds_positions.keys():
                out.write(functions["sound"].to_bytes(1, "big"))
                out.write(sounds_positions[t[0]].to_bytes(2, "big"))
                if len(t) > 1:
                    if int(t[1]) == -1:
                        out.write(int(255).to_bytes(1, "big"))
                    else:
                        out.write(int(t[1]).to_bytes(1, "big"))
                else:
                    out.write(int(1).to_bytes(1, "big"))
            elif t[0] == "~":
                out.write(functions["sound"].to_bytes(1, "big"))
                out.write(int(32700).to_bytes(2, "big"))
                out.write(int(1).to_bytes(1, "big"))
            pass
        elif c == "music":
            t = line.replace("music ", "", 1).replace("\n", "").replace("\t", " ").strip().split(" ")
            t[0] = os.path.splitext(t[0])[0]
            if t[0] in music_positions.keys():
                out.write(functions["music"].to_bytes(1, "big"))
                out.write(int(music_positions[t[0]]).to_bytes(2, "big"))
            else:
                out.write(functions["music"].to_bytes(1, "big"))
                out.write(int(novel_stop_music).to_bytes(2, "big"))
            pass
        elif c == "text":
            lines_count +=1
            t = line.replace("text ", "", 1).replace("\n", "").replace("\t", " ").lstrip()
            if len(t) == 0 or t[0] == "~":
                continue
            out.write(functions["text"].to_bytes(1, "big"))
            out.write(t.encode())
            out.write((0).to_bytes(1, "big"))
        elif c == "choice":
            out.write(functions["choice"].to_bytes(1, "big"))
            choice = line.replace("choice ", "", 1).replace("\n", "").replace("\t", " ").split("|")
            out.write(len(choice).to_bytes(1, "big"))
            for c in choice:
                out.write(c.strip().encode())           
                out.write((0).to_bytes(1, "big"))
        elif c == "setvar" or c == "gsetvar":
            coms[1] = coms[1].lower()
            if (coms[1] == "~"):
                out.write(functions["reset_vars"].to_bytes(1, "big"))
                continue
            out.write(functions["setvar"].to_bytes(1, "big"))
            try:
                out.write(script_var[coms[1]].to_bytes(2, "big"))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("Variable " + coms[1] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists\n")
                exit()
            if (coms[2] == "="):
                out.write(int(0).to_bytes(1, "big"))
            elif (coms[2] == "+"):
                out.write(int(1).to_bytes(1, "big"))
            elif (coms[2] == "-"):
                out.write(int(2).to_bytes(1, "big"))
            else:
                print("\n\n\n------------------- ERROR------------------")
                print("Unknown symbol " + coms[2] + " in script \"" + script_file + "\", line " + str(i+1) +"\n")
                exit()
            if coms[3].isnumeric():
                out.write(int(coms[3]).to_bytes(2, "big"))
                # 0 it is a number to be added at the var
                out.write(int(0).to_bytes(1, "big"))
            else:
                
                coms[3] = coms[3].lower()
                if '"' in coms[3]: #It is a string so it is a .scr file or a label
                    coms[3] = coms[3].replace('"', "")
                    if ".scr" in coms[3]: #It is a .scr file
                        try:
                            key = coms[3].lower().replace(".scr", "")
                            out.write(int(scripts_dir[key]).to_bytes(2, "big"))
                            out.write(int(0).to_bytes(1, "big"))
                        except:
                            print(script_var)
                            print("\n\n\n------------------- ERROR------------------")
                            print("The .scr " + coms[3] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                            exit()
                    else:
                        try:
                            alias = get_novel_script_alias(script_file)
                            key = coms[3].lower()
                            out.write(int(script_label[alias][key]).to_bytes(2, "big"))
                            out.write(int(0).to_bytes(1, "big"))
                        except:
                            print(script_var)
                            print("\n\n\n------------------- ERROR------------------")
                            print("The label " + coms[3] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                            exit()
                else:
                    try:
                        out.write(int(script_var[coms[3]]).to_bytes(2, "big"))
                        #1 it is another var to be added at the var
                        out.write(int(1).to_bytes(1, "big"))
                    except:
                        print(script_var)
                        print("\n\n\n------------------- ERROR------------------")
                        print("The var " + coms[3] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                        exit()
            pass
        elif c == "gset_var":
            pass
        elif c == "if":
            out.write(functions["if"].to_bytes(1, "big"))
            #next is the type of the right hand value number or var
            t = line.replace("if ", "", 1).replace("\n", "").replace("\t", " ").split(" ")
            #out.write(int(script_var[t[0]]).to_bytes(2, "big"))
            try:
                out.write(int(script_var[coms[1].lower()]).to_bytes(2, "big"))
            except:
                print(script_var)
                print("\n\n\n------------------- ERROR------------------")
                print("The var " + coms[1] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                exit()
            if coms[2] == "==":
                out.write((0).to_bytes(1, "big"))
            elif t[1] == "!=":
                out.write((1).to_bytes(1, "big"))
            elif t[1] == ">":
                out.write((2).to_bytes(1, "big"))
            elif t[1] == "<":
                out.write((3).to_bytes(1, "big"))
            elif t[1] == ">=":
                out.write((4).to_bytes(1, "big"))
            elif t[1] == "<=":
                out.write((5).to_bytes(1, "big"))
            else:
                print(line)
                exit()
            coms[3] = coms[3].replace(":", "") #Using : makes it easier to right if selections cause it behaves like python in the vscode
            #print(coms)
            if coms[3].isnumeric():
                out.write(int(coms[3]).to_bytes(2, "big"))
                out.write((0).to_bytes(1, "big"))
            elif '"' in coms[3]:
                key = coms[3].replace('"', "").replace(".scr", "").strip()
                print(key)
                try:
                    out.write(int(scripts_dir[key]).to_bytes(2, "big"))
                except:
                    print(script_var)
                    print("\n\n\n------------------- ERROR------------------")
                    print("The .scr " + coms[3] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                    exit()
                out.write((0).to_bytes(1, "big"))
            else:
                try:
                    out.write(int(script_var[coms[3]]).to_bytes(2, "big"))
                except:
                    print(script_var)
                    print("\n\n\n------------------- ERROR------------------")
                    print("The var " + coms[3] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                    exit()
                out.write((1).to_bytes(1, "big"))
            try:
                out.write(count_to_fi(lines, i+1, 0).to_bytes(2, "big"))
            except:
                print(scripts_dir)
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe if in script \"" + script_file + "\", line " + str(i+1) + " does not have fi.")
                exit()
            pass
        elif c == "fi":
            out.write(functions["fi"].to_bytes(1, "big"))
            pass
        elif c == "jump":
            t = line.replace("\t", "").replace("jump ", "", 1).lower().replace("\n", "").replace("/", "_").replace(".scr", "").split(" ")
            key = t[0].replace("-", "_").lower()
            if (key[0] == "$"):
                out.write(functions["retjump"].to_bytes(1, "big"))
                if len(t) > 1:
                    if t[1][0] != "$":
                        print(scripts_dir)
                        print("\n\n\n------------------- ERROR------------------")
                        print("\nThe jump ret can have only $ labels\"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                        exit()
                    out.write((0).to_bytes(1, "big"))
                    out.write(script_var[key.replace("$", "").strip()].to_bytes(2, "big"))
                    out.write(int(script_var[t[1].replace("$", "").strip()]).to_bytes(2, "big"))
                    out.write((0).to_bytes(1, "big")) #Extra one 0 to have the same size with regular jump
                else:
                    out.write((1).to_bytes(1, "big"))
                    out.write(script_var[key.replace("$", "").strip()].to_bytes(2, "big"))
                    out.write((0).to_bytes(2, "big"))
                    out.write((0).to_bytes(1, "big")) #Extra one 0 to have the same size with regular jump
            else:
                out.write(functions["jump"].to_bytes(1, "big"))
                try:
                    out.write(scripts_dir[key].to_bytes(2, "big"))
                except:
                    print(scripts_dir)
                    print("\n\n\n------------------- ERROR------------------")
                    print("\nThe jump \"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                    exit()
                if len(t) > 1:
                    num = int(script_label[key][t[1].lower().strip()])
                    out.write(num.to_bytes(4, "big", signed=True))
                else:
                    out.write(int(0).to_bytes(4, "big", signed=True))
                    pass
        elif c == "delay":
            out.write(functions["delay"].to_bytes(1, "big"))
            try:
                out.write(int(coms[1]).to_bytes(2, "big", signed=True))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe delay \"" + str(coms[1]) + "\" in script \"" + script_file + "\", line " + str(i+1) + " is too big.")
                exit()
            pass
            
        elif c == "random":
            print(line)
            pass
        elif c == "label":
            pass
        elif c == "goto":
            out.write(functions["goto"].to_bytes(1, "big"))
            t = line.replace("goto ", "", 1).lower().replace("\n", "", 1).replace("\t", "", 1).replace("/", "_").replace(".scr", "").split(" ")
            alias = get_novel_script_alias(script_file)
            try:
                pos = script_label[alias][t[0]]
                out.write(pos.to_bytes(4, "big", signed=True))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe goto \"" + t[0] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                exit()
            
            
            pass
        elif c == "cleartext":
            print(line)
            pass
        elif c == "ifchoice":
            out.write(functions["ifchoice"].to_bytes(1, "big"))
            choice = line.replace("ifchoice ", "", 1).replace("\n", "").replace("\t", " ").split("|")
            out.write(len(choice).to_bytes(1, "big"))
            #types of is choice 0 no if 1 if
            #types of right hand is 0 for numbers 1 for var
            #the left hand number of var
            #the number of the var if it is var or the actual number
            #: separates ifs from the text of the choice
            #ifs 0 -> ==  |  1 -> !=  |  2 -> >  |  3 -> <   |   4 -> >=   |   5 -> <=
            for c in choice:
                ifs = c.split(":")
                if len(ifs) == 1:

                    out.write((0).to_bytes(1, "big"))
                    out.write((0).to_bytes(1, "big"))
                    out.write((0).to_bytes(2, "big"))
                    out.write((0).to_bytes(2, "big"))
                    out.write((0).to_bytes(1, "big"))

                    out.write(c.strip().encode())           
                    out.write((0).to_bytes(1, "big"))
                else:
                    out.write((1).to_bytes(1, "big"))
                    
                    parts = ifs[0].strip().split(" ")
                    #print(parts)
                    if len(parts) < 3: #just a variable so it will return true if it is != 0
                        out.write((0).to_bytes(1, "big"))
                        try:
                            out.write(script_var[parts[0].strip()].to_bytes(2, "big"))
                        except:
                            print("\n\n\n------------------- ERROR------------------")
                            print("\nThe var in ifchoice \"" + parts[2] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                            exit()
                        out.write((1).to_bytes(1, "big"))
                    else:
                        if parts[2].isnumeric():
                            out.write((0).to_bytes(1, "big"))
                            try:
                                out.write(script_var[parts[0].strip()].to_bytes(2, "big"))
                            except:
                                print("\n\n\n------------------- ERROR------------------")
                                print("\nThe var in ifchoice \"" + parts[2] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                                exit()
                            out.write(int(parts[2].strip()).to_bytes(2, "big"))
                        else:
                            
                            if '"' in parts[2]: #It is a script file... srcipt labels are no accepted
                                out.write((0).to_bytes(1, "big"))
                                try:
                                    out.write(int(script_var[parts[0].strip()]).to_bytes(2, "big"))
                                except:
                                    print("\n\n\n------------------- ERROR------------------")
                                    print("\nThe var in ifchoice \"" + parts[2] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                                    exit()
                                scr = parts[2].lower().replace(".scr", "").replace('"', "").strip()
                                print(scr)
                                print(parts)
                                print(scripts_dir[scr])
                                print(scripts_dir)
                                
                                try:
                                    out.write(int(scripts_dir[scr]).to_bytes(2, "big"))
                                except:
                                    print(scripts_dir)
                                    print("\n\n\n------------------- ERROR------------------")
                                    print("The ifchoice .scr " + parts[2] + " in script \"" + script_file + "\", line " + str(i+1) + " does not exists")
                                    exit()
                            else:
                                out.write((1).to_bytes(1, "big"))
                                try:
                                    out.write(int(script_var[parts[0].strip()]).to_bytes(2, "big"))
                                except:
                                    print("\n\n\n------------------- ERROR------------------")
                                    print("\nThe var in ifchoice \"" + parts[2] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                                    exit()
                                try:
                                    out.write(int(script_var[parts[2].strip()]).to_bytes(2, "big"))
                                except:
                                    print("\n\n\n------------------- ERROR------------------")
                                    print("\nThe var in ifchoice \"" + parts[2] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                                    exit()
                        comp = parts[1].strip()
                        if comp == "==":
                            out.write((0).to_bytes(1, "big"))
                        elif comp == "!=":
                            out.write((1).to_bytes(1, "big"))
                        elif comp == ">":
                            out.write((2).to_bytes(1, "big"))
                        elif comp == "<":
                            out.write((3).to_bytes(1, "big"))
                        elif comp == ">=":
                            out.write((4).to_bytes(1, "big"))
                        elif comp == "<=":
                            out.write((5).to_bytes(1, "big"))
                        else:
                            print("\n\n\n------------------- ERROR------------------")
                            print("\nThe comparison in ifchoice \"" + parts[1] + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                            exit()
                        
                    #print(ifs[1])
                    out.write(ifs[1].strip().encode())           
                    out.write((0).to_bytes(1, "big"))
        else:
            ############### EXTERNAL FUNCTIONS
            func = line.split(" ")[0].strip()
            if func in external_funcs:
                out.write(functions["external_func"].to_bytes(1, "big"))
                out.write(external_funcs[func].to_bytes(1, "big"))
    #print(script_file)
    #print(bytes_count)
    script.close()
    out.close()
    alias = out_file.replace("res\\", "", 1).replace("\\", "_").replace(".bin", "").replace(".", "_")
    #script_res.write("BIN " + alias + " " + out_file.replace("res\\", "", 1) + " 2 2 0 NONE FALSE\n")
    script_res.write("BIN " + alias + " " + out_file.replace("res\\", "", 1) + "\n")
    
    if alias != "script_main":
        scripts_c.write("\t" + alias + ",\n")
        script_byte_count.append(bytes_count)
    else:
        script_byte_count.insert(0,bytes_count)

scripts_c.write("};\n\n")
#scripts_h.write("extern const s32 NOVEL_SCRIPTS_BYTES_COUNT[];\n\n")
scripts_c.write("const s32 NOVEL_SCRIPTS_BYTES_COUNT[] = {\n")
for value in script_byte_count:
    scripts_c.write("\t" + str(value) + ",\n")
scripts_c.write("};\n\n")
scripts_c.close()




variables_h = open("inc/novel_variables.h", "w")
variables_h.write("#ifndef H_NOVEL_VARIABLES\n")
variables_h.write("#define H_NOVEL_VARIABLES\n\n")
variables_h.write("extern const int NOVEL_SAVE_CHECK_NUM;\n\n")
variables_h.write("extern const int NOVEL_NUM_VARIABLES;\n")
variables_h.write("extern const int NOVEL_NUM_GLOBAL_VARIABLES;\n")
variables_h.write("extern int NOVEL_VARIABLES[];\n\n")

variables_h.write("\n\n")
variables_h.write("//VARABLES\n")
for var in script_var:
    variables_h.write("#define NVAR_" + var + " NOVEL_VARIABLES[" + str(script_var[var])+ "]\n")

variables_h.write("\n\n")
variables_h.write("//FILES\n")
for scr in scripts_dir:
    variables_h.write("#define NFILE_" + scr + " " + str(scripts_dir[scr])+ "\n")

variables_h.write("\n\n")
variables_h.write("//LABELS\n")
for scr in script_label:
    for label in script_label[scr]:
        variables_h.write("#define NLABEL_" + scr + "_" + label + " " + str(script_label[scr][label])+ "\n")
variables_h.write("\n\n")

if not bad_filenames:
    variables_h.write("\n\n")
    variables_h.write("//BACKGROUNDS\n")
    for bg in backgrounds:
        variables_h.write("#define NBG_" + bg.replace(".png", "").replace(".jpg", "").strip() + " " + str(backgrounds[bg])+ "\n")
    variables_h.write("\n\n")

    variables_h.write("\n\n")
    variables_h.write("//FOREGROUNDS\n")
    for fg in foregrounds:
        variables_h.write("#define NFG_" + fg.replace(".png", "").replace(".jpg", "").strip() + " " + str(foregrounds[fg])+ "\n")
    variables_h.write("\n\n")
else:
    variables_h.write("//BAD FILENAMES\n")
    variables_h.write("\n\n")

variables_h.write("\n#endif\n")
variables_h.close()

var_c = open("src/novel_variables.c", "w")
var_c.write("#include \"novel_variables.h\"\n")
var_c.write("#include \"novel_external_functions.h\"\n\n")
var_c.write("const int NOVEL_SAVE_CHECK_NUM = " + str(save_check) + ";\n\n")
var_c.write("const int NOVEL_NUM_VARIABLES = " + str(len(script_var)) + ";\n")
var_c.write("const int NOVEL_NUM_GLOBAL_VARIABLES = " + str(num_global_var) + ";\n\n")
var_c.write("int NOVEL_VARIABLES[" + str(len(script_var)) + "];\n")
var_c.write("void (*nv_external_functions[])() = {\n")
for func in external_funcs:
    var_c.write("\t" + func + ",\n")
var_c.write("};")
var_c.close()


if len(script_var) == 1:
    print("----------------------------")
    print("A Novel without Variables")

#print(music_positions)
print(script_var)

print("Lines of text : " + str(lines_count))