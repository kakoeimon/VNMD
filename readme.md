# VNMD early version

**VNMD** is a tool for converting [VNDS](https://github.com/BASLQC/vnds) Visual Novels to a rom (.bin) to be used on **Sega Mega Drive** thanks to [SGDK](https://github.com/Stephane-D/SGDK).


 
## Setup

This works only on Windows.

First you will need to install [SGDK](https://github.com/Stephane-D/SGDK/releases/tag/v1.70) (version this repo used is 1.70 ) Probably it will be best if you instal SGDK at c:\sgdk

Next you will need [Python3](https://www.python.org/downloads/). Probably you already have this so check it in your Command Prompt by typing: python --version.

You will also need [PILLOW](https://pillow.readthedocs.io/en/stable/installation.html) for Python. Use pip commands to install it.

Then Optionaly but for much better quality, install [ImageMagick](https://imagemagick.org/script/download.php) and when you install check the convert legacy.

Last you will need a VNDS visual novel the list is [here](https://github.com/BASLQC/vnds/wiki/List-of-VNDS-Visual-Novels)
* Prefer to download SD versions of the Novels.
* Warning : Many Novels in this list are broken. Some contain Japanese characters or not standard character, others are just realy bad ports. For testing purposes I suggest to download the "The Best Eroge Ever"


Extract this repo to a dir. inside this dir create a novel directory and extract the novel.
Inside the novel dir you will have directories named background, foreground and scr among others.
Some novels have those directories zipped unzip them.

Note
* all novel extractions must be made without creating a directory with the name of the zip.

Last open the novel.ini
````
MAGICK_CONVERT_PATH C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert.exe
BG_WIDTH 32
BG_HEIGHT 24
BG_TOP 0
TEXT_TOP 24
TEXT_BOTTOM 28
TEXT_LEFT 2
TEXT_RIGHT 38
COMPRESSION APLIB
SAVE_CHECK 1123
SOUND_DRV 2ADPCM
````
If you installed ImageMagick find the convert.exe that it was installed with your ImageMagick and replace the full file path at MAGICK_CONVERT_PATH with yours. Additionally you can leave the path empty or pointing not to a file to use just PILLOW for the convertion of the graphics. But Image Magick gives much better quality.

Now you are ready to convert.

## Convert a novel
Open a command prompt and navigate to the dir you unziped this repo.
run
````
python convert_images.py
````
This will create a res dir and will convert the images of the Novel.
This will take some time if the novel is big.

Then run
````
python create_image_res.py
````
This will create the .res files for SGDK and some C files that will be needed for the rom.

Then run.
````
python convert_scripts.py
````
This will convert the scripts to binaries and will create .res files and C files.
Also with this command you can fins problems to a broken novel eaisier.

If you got no errors till now.

Run.
````
build.bat
````
This will build everything to the final rom


### Warning 
If the rom.bin is bigger than 4 MB then you will have to compile the SGDK to force it to use Bank Switching otherwise MD will crash.
 
So if this is the case you will have to go to the directory you installed SGDK and inside the inc directory locate and open the file config.h
in this file find this line
````
#define ENABLE_BANK_SWITCH  0
````
and change it to
````
#define ENABLE_BANK_SWITCH  1
````
then run from the SGDK's dir this file
````
build_lib.bat
````
The opposite must be made if Bank Switching is enabled and the rom is less than 4MB

## novel.ini
The novel.ini is like this
````
MAGICK_CONVERT_PATH C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert.exe
BG_WIDTH 32
BG_HEIGHT 24
BG_TOP 0
TEXT_TOP 24
TEXT_BOTTOM 28
TEXT_LEFT 2
TEXT_RIGHT 38
COMPRESSION APLIB
SAVE_CHECK 1123
SOUND_DRV 2ADPCM
````
* MAGICK_CONVERT_PATH is the path to the convert.exe if the path does not point to a file PILLOW will be used to convert the Images.
* BG_WIDTH is the width you want the image to be in tiles (one tile is 8px)
* BG_HEIGHT is the height you want the image to be in tiles (one tile is 8px)
* BG_TOP where the image is going to be drawn and this is the top part (one tile is 8px)
* TEXT_TOP from where your text is going to be drawn in tiles (one tile is 8px) 
* TEXT_BOTTOM the bottom of the text in tiles (one tile is 8px)
* TEXT_LEFT the left side of the text in tiles (one tile is 8px) 
* TEXT_RIGHT the left side of the text in tiles (one tile is 8px) 
* COMPRESSION the compresion SGDK is going to use for the images. The options are.
* * NONE no compression
* * FAST fast but sometimes buggy. Avoid.
* * APLIB slow but good compression.
* SAVE_CHECK This is just a number to help the program with the saving option change it to what ever you want as long it is bigger than 0 and smaller than 32767 also it may be better to use a number with more than two digits.
* SOUND_DRV as sound driver you want to use. Consider reading the SGDK info about this. Also you have to put the sound fx in a directory name wav and the music in a directory name music. The options are.
* * 2ADPCM
* * 4PCM
* * XGM
* 

* * String Vars
* VNDS can have string vars that can be used inside the text or as vars that hold script files or labels
* VNMD can have string vars but you cannot use them inside the text.
* String vars can be script files or labels (labels can be only labels of the working file)

* e.g.
* setvar retfile = "office.scr" (you can add any existing .scr file)
* jump $retfile  (when you jump with string vars you can only use string vars for labels or nothing)

* e.g.
* setvar retfile2 = "main.scr"
* setvar retlabel2 = "second_day" (this will work only if it is written in the main.scr and the main.scr have a label second_day)
* jump $retfile2 $retlabel2

### So that's all... good luck in converting
Many VNDS Novels require work to make them run.

### Updating SGDK
If you update SGDK be sure to delete the boot dir inside the scr dir, otherwise the project will not compile.


## TODO
* Add random command
* Add external_function command
* * With an external function command we will have the ability to call C functions from the Script and get the control of the Novel.

