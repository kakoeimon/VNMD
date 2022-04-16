import os
import glob
from random import choices
from PIL import Image
import sys

from numpy import var

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
        count += 0
    elif c == "music":
        count += 0
    elif c == "text":
        t = line.replace("text ", "", 1).replace("\n", "").replace("\t", " ").lstrip()
        if len(t) == 0 or t[0] == "~":
            return 0
        count += len(t) + 2
    elif c == "choice":
        count +=2
        choice = line.replace("choice ", "", 1).replace("\n", "").replace("\t", " ").split("|")
        for c in choice:
            count += len(c) + 1
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
        count += 7
    elif c == "dealy":
        count += 0
    elif c == "random":
        count += 0
    elif c == "label":
        count += 0
    elif c == "goto":
        count += 5
    elif c == "cleartext":
        count += 0
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
            "if":8, "fi":9, "jump":10, "dealy":11, "random":12,
            "label":13, "goto": 14, "cleartext": 15 , "reset_vars": 16,

}

def get_novel_script_alias(script_file):
    f = script_file.replace("res\\", "", 1).replace(".scr", "")
    
    alias = f.replace("\\", "_").replace("novel_script_", "", 1)
    return alias

backgrounds = {}
for bg_file in glob.glob('novel/background/**/*.jpg', recursive=True):
    backgrounds[bg_file.replace("novel/background\\", "", 1).replace("\\", "/").replace("/", "_").replace("-", "_").lower()] = len(backgrounds)
for bg_file in glob.glob('novel/background/**/*.png', recursive=True):
    backgrounds[bg_file.replace("novel/background\\", "", 1).replace("\\", "/").replace("/", "_").replace("-", "_").lower()] = len(backgrounds)

foregrounds = {}
for fr_file in glob.glob('novel/foreground/**/*.png', recursive=True):
    foregrounds[fr_file.replace("novel/foreground\\", "").replace("\\", "/").replace("/", "_").replace("-", "_").lower()] = len(foregrounds)

if not os.path.exists('res/script'):
    os.mkdir('res/script')

scripts_h = open("inc\\novel_scripts.h", "w")
scripts_h.write("#ifndef H_NOVEL_SCRIPTS\n")
scripts_h.write("#define H_NOVEL_SCRIPTS\n\n")
scripts_h.write("#include \"genesis.h\"\n")
scripts_h.write("#include \"scripts_res.h\"\n\n")
scripts_h.write("extern const u8* NOVEL_SCRIPTS[];\n\n")
scripts_h.write("extern const s32 NOVEL_SCRIPTS_BYTES_COUNT[];\n\n")
scripts_h.write("\n#endif\n")


scripts_c = open("src\\novel_scripts.c", "w")
scripts_c.write("#include \"novel_scripts.h\"\n\n")
scripts_c.write("const u8* NOVEL_SCRIPTS[] = {\n")
scripts_c.write("\tscript_main,\n")


script_res = open("res\\scripts_res.res", "w")

scripts_dir = {"main":0}
script_label = {}
script_var = {"selected":0}
script_byte_count = []
tmp_var = {}
tmp_global_var = {}
for script_file in glob.glob('novel\\script\\*.scr', recursive=False):

    alias = get_novel_script_alias(script_file)
    script_label[alias] = {}
    try:
        lines = open(script_file, 'r').readlines()
    except Exception as e:
        print("------------------ ERROR ---------------")
        print("at file " + script_file)
        print(e)
        exit()
    
    bytes_count = 0
    for i in range(len(lines)):
        line = lines[i].lstrip()
        l = line.replace("\t", " ").replace("\n", " ").replace(":", " ").split()
        bytes_count += count_line(lines, i)
        #print(l)
        
        if len(l) == 0:
            pass
        elif l[0] == "label":
            script_label[alias][l[1].lower()] = bytes_count
        elif l[0] == "gsetvar":
            if l[1] not in tmp_global_var.keys() and l[1] != "selected":
                tmp_global_var[l[1]] = len(tmp_global_var)
        elif l[0] == "setvar":
            if l[1] != "~" and l[1] not in tmp_var.keys() and l[1] != "selected":
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

#print(script_var)

#print(script_label)

for script_file in glob.glob('novel\\script\\*.scr', recursive=False):
    f = script_file.replace("res\\", "", 1).replace(".scr", "")
    
    alias = f.replace("\\", "_").replace("novel_script_", "", 1).replace("-", "_").lower()
    
    if alias != "main":
        scripts_dir[alias] = len(scripts_dir)


#print(scripts_dir)


for script_file in glob.glob('novel\\script\\*.scr', recursive=False):
    bytes_count = 0
    script = open(script_file, 'r')
    out_file = script_file.replace("novel\\", "res\\").replace(".scr", ".bin").replace("-", "_")
    #print(out_file)
    out = open(out_file, 'wb')
    lines = script.readlines()

    for i in range(len(lines)):
        #lines[i] = lines[i].lstrip()
        line = lines[i].lstrip()
        coms = line.split()
        
        bytes_count += count_line(lines, i)
        c = line.split(" ")[0].replace("\n", "").replace("\t", "")
        if c == "bgload":
            out.write(functions["bgload"].to_bytes(1, "big"))
            t = line.replace("bgload ", "", 1).lower().replace("\n", "", 1).replace("\t", "", 1).replace("/", "_").replace("-", "_").split(" ")
            key = t[0]
            try:
                out.write(backgrounds[key].to_bytes(2, "big"))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe background image \"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                #print(backgrounds.keys())
                #out.write(backgrounds[backgrounds.keys().0].to_bytes(1, "big"))
                exit()
            if len(t) == 2 and t[1].isnumeric():
                out.write(int(t[1]).to_bytes(2, "big"))
            else:
                out.write((16).to_bytes(2, "big"))
            
            
        elif c == "setimg":
            out.write(functions["setimg"].to_bytes(1, "big"))
            t = line.replace("setimg ", "", 1).lower().replace("\n", "", 1).replace("\t", "", 1).replace("/", "_").split(" ")
            key = t[0].replace("-", "_")
            try:
                out.write(foregrounds[key].to_bytes(2, "big"))
            except:
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe foreground image \"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                exit()
            if len(t) > 1:
                x = int((float(t[1]) * img_scale) / 8 + bg_left)
                out.write(x.to_bytes(2, "big", signed=True))
            else:
                out.write(int(0).to_bytes(2, "big", signed=True))
            if len(t) > 2:
                y = int((float(t[2]) * img_scale) / 8 + bg_top)
                out.write(y.to_bytes(2, "big", signed=True))
            else:
                out.write(int(0).to_bytes(2, "big", signed=True))
        elif c == "sound":
            pass
        elif c == "music":
            pass
        elif c == "text":
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
                out.write(c.encode())           
                out.write((0).to_bytes(1, "big"))
        elif c == "setvar" or c == "gsetvar":
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
                out.write(int(0).to_bytes(1, "big"))
            else:
                try:
                    out.write(int(script_var[coms[3]]).to_bytes(2, "big"))
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
                out.write(int(script_var[coms[1]]).to_bytes(2, "big"))
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
            if coms[3].isnumeric():
                out.write(int(coms[3]).to_bytes(2, "big"))
                out.write((0).to_bytes(1, "big"))
            else:
                out.write(int(script_var[coms[3]]).to_bytes(2, "big"))
                out.write((1).to_bytes(1, "big"))
            out.write(count_to_fi(lines, i+1, 0).to_bytes(2, "big"))
            pass
        elif c == "fi":
            out.write(functions["fi"].to_bytes(1, "big"))
            pass
        elif c == "jump":
            out.write(functions["jump"].to_bytes(1, "big"))
            t = line.replace("\t", "").replace("jump ", "", 1).lower().replace("\n", "").replace("/", "_").replace(".scr", "").split(" ")
            key = t[0].replace("-", "_")
            try:
                out.write(scripts_dir[key].to_bytes(2, "big"))
            except:
                print(scripts_dir)
                print("\n\n\n------------------- ERROR------------------")
                print("\nThe jump \"" + key + "\" in script \"" + script_file + "\", line " + str(i+1) + " does not exists.")
                exit()
            if len(t) > 1:
                num = int(script_label[t[0]][t[1]])
                out.write(num.to_bytes(4, "big", signed=True))
            else:
                out.write(int(0).to_bytes(4, "big", signed=True))
                pass
        elif c == "dealy":
            print(line)
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
            pos = script_label[alias][t[0]]
            out.write(pos.to_bytes(4, "big", signed=True))
            pass
        elif c == "cleartext":
            print(line)
            pass
    
    #print(script_file)
    #print(bytes_count)
    script.close()
    out.close()
    alias = out_file.replace("res\\", "", 1).replace("\\", "_").replace(".bin", "")
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
variables_h.write("extern int NOVEL_VARIABLES[];\n")
variables_h.write("\n#endif\n")
variables_h.close()

var_c = open("src/novel_variables.c", "w")
var_c.write("#include \"novel_variables.h\"\n\n")
var_c.write("const int NOVEL_SAVE_CHECK_NUM = " + str(save_check) + ";\n\n")
var_c.write("const int NOVEL_NUM_VARIABLES = " + str(len(script_var)) + ";\n")
var_c.write("const int NOVEL_NUM_GLOBAL_VARIABLES = " + str(num_global_var) + ";\n\n")
var_c.write("int NOVEL_VARIABLES[" + str(len(script_var)) + "];\n")
var_c.close()

if len(script_var) == 1:
    print("----------------------------")
    print("A Novel without Variables")

print(script_var)