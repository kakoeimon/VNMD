REM del /s /q %cd%\out\

c:\sgdk\bin\make -f c:\sgdk\makefile.gen

C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\blastem_libretro.dll %cd%\out\rom.bin
REM c:\sgdk\emu\blastem\blastem.exe %cd%\out\rom.bin

REM C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\genesis_plus_gx_libretro.dll %cd%\out\rom.bin
REM C:\Users\kakoeimon\AppData\Roaming\RetroArch\RetroArch.exe -L C:\Users\kakoeimon\AppData\Roaming\RetroArch\cores\blastem_libretro.dll %cd%\out\rom.bin
