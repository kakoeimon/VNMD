del %cd%\out\rom.bin

python convert_scripts.py
c:\sgdk\bin\make -f c:\sgdk\makefile.gen

REM CHANGES THIS LINE WITH YOUR EMULATOR
C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\blastem_libretro.dll %cd%\out\rom.bin
