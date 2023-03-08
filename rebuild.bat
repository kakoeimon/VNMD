del %cd%\out\rom.bin

python create_external_functions.py
python convert_scripts.py
c:\sgdk\bin\make -f c:\sgdk\makefile.gen

c:\RetroArch-Win64\retroarch.exe -L c:\RetroArch-Win64\cores\blastem_libretro.dll out\rom.bin
REM c:\sgdk\emu\blastem\blastem.exe %cd%\out\rom.bin

REM C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\genesis_plus_gx_libretro.dll %cd%\out\rom.bin
REM C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\blastem_libretro.dll %cd%\out\rom.bin
