# VNMD early version

**VNMD** is a tool for converting [VNDS](https://github.com/BASLQC/vnds) Visual Novels to a rom (.bin) to be used on **Sega Mega Drive** thanks to [SGDK](https://github.com/Stephane-D/SGDK).


 
## Setup

This works only on Windows.

First you will need to install [SGDK](https://github.com/Stephane-D/SGDK/releases/tag/v1.70) (version this repo used is 1.70 ) Probably it will be best if you instal SGDK at c:\sgdk

Then [ImageMagick](https://imagemagick.org/script/download.php) and when you install check the convert legacy.

Next you will need [Python3](https://www.python.org/downloads/). Probably you already have this so check it in your Command Prompt by typing: python --version.

You will also need [PILLOW](https://pillow.readthedocs.io/en/stable/installation.html) for Python. Use pip commands to install it.

Then you will need a VNDS visual novel the list is [here](https://github.com/BASLQC/vnds/wiki/List-of-VNDS-Visual-Novels)
* Prefer to download SD versions of the Novels.
* Warning : Many Novels in this list are broken. Some contain Japanese characters or not standard character, others are just realy bad ports. For testing purposes I suggest to download the "The Best Eroge Ever"


Extract this repo to a dir. inside this dir create a novel directory and extract the novel.
Inside the novel dir you will have directories named background, foreground and scr among others.
Some novels have those directories zipped unzip them.

Note
* all extractions must be made without creating a directory with the name of the zip.

Last open the novel.ini
````
MAGICK_CONVERT_PATH C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert
BG_WIDTH 32
BG_HEIGHT 24
BG_TOP 0
TEXT_TOP 24
TEXT_BOTTOM 28
TEXT_LEFT 2
TEXT_RIGHT 38
COMPRESSION APLIB
SAVE_CHECK 1123
````
Find the convert.exe that it was installed with your ImageMagick and replace the path at MAGICK_CONVERT_PATH with yours.

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
But here is and were you are going to get the errors if an image is problematic.
For some reason black and white images do not convert well (this is on the todo list)
One solution is add some colors on it or change the hue.
So if the game does not compile and tou get an error search for the name of the failed image fix it with extra colors othe that gray scale and run.
````
python convert_images.py local path to the image
````
for example
````
python convert_images.py novel\background\IMG_10.jpg
````
Then build again and repeat until you have no errors.
If this happens open the dir out and inside you will find the file out.bin. This is your rom.

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
MAGICK_CONVERT_PATH C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert
BG_WIDTH 32
BG_HEIGHT 24
BG_TOP 0
TEXT_TOP 24
TEXT_BOTTOM 28
TEXT_LEFT 2
TEXT_RIGHT 38
COMPRESSION APLIB
SAVE_CHECK 1123
````
* MAGICK_CONVERT_PATH is the path to the convert.exe
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


### So that's all... good luck in converting
Many VNDS Novels require work to make them run.


## TODO and Ask for help
Probably the best way will had been not to use an external to Python program to do the image conversion. Doing all this with PILLOW would had been ideal but I can't get PILLOW to save an image with only 16 indexed colors it always expands the colors to 256 so if someone knows how to do this please inform me.
Also another thing I want to find is to find a way for ImageMagick to save and the gray scaled images to 16 indexed colors but I do not know how to do it.

Add music.
Music files cannot be converted to MD's format but make the converter to check for an XGM file with the same name in the script to add and use it.
