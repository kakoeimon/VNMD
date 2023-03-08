h_out = open("inc\\novel_external_functions.h", "w")

c_in = open("src\\novel_external_functions.c", "r")

funcs = []
for line in c_in.readlines():
    if line[:5] == "void ":
        f = line[5:].replace("(", "").replace(")", "").replace("{", "").strip()
        funcs.append(f)

print(funcs)

h_out.write("#ifndef H_NV_EXTERNAL_FUNCTIONS\n")
h_out.write("#define H_NV_EXTERNAL_FUNCTIONS\n\n")

h_out.write("#define NV_EXTERNAL_FUNCTIONS_NUM " + str(len(funcs)) + "\n\n")

h_out.write("extern void (*nv_external_functions[])();\n\n")

for f in funcs:
    h_out.write("void " + f + "();\n")

h_out.write("\n#endif\n")