import os
from glob import glob


for d in glob('novel\\script\\**\\*\\', recursive=True):
    d = d.replace("script", "grscript", 1)
    if not os.path.exists(d):
        os.mkdir(d)

for script_file in glob('novel\\script\\**\\*.scr', recursive=True):
    print(script_file)