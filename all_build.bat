del %cd%\out\rom.bin
del %cd%\out\res\resources.o
python stages.py

%GDK_WIN%\bin\make -f %GDK_WIN%\makefile.gen

REM %GDK_WIN%\emu\fusion\Fusion.exe %cd%\out\rom.bin
REM %GDK_WIN%\emu\gens\gens.exe %cd%\out\rom.bin
REM %GDK_WIN%\emu\blastem\blastem.exe %cd%\out\rom.bin
REM %GDK_WIN%\emu\genplus\gen_sdl.exe %cd%\out\rom.bin
C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\genesis_plus_gx_libretro.dll %cd%\out\rom.bin
REM C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\blastem_libretro.dll %cd%\out\rom.bin
