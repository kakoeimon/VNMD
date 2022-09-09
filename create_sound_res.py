from ctypes import sizeof
import glob
import shutil
from pydub import AudioSegment
from pydub.utils import mediainfo
import pathlib
import soundfile as sf

import os

###############################################
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
sound_drv = ini.readline().replace("SOUND_DRV ", "").replace("\n", "").strip()
################################################

exec('if os.path.isdir("res\wav"):\n\tshutil.rmtree("res\wav")\nos.mkdir("res\wav")')



sound_res = open("res\\novel_sounds_res.res", 'w')


sound_res.write("NEAR\n")

sounds_c = open("src/novel_sounds.c", 'w')
sounds_c.write("#include \"novel_sounds.h\"\n\n")

sounds_c.write("void novel_stop_sound() {\n")
if sound_drv == "XGM":
    sounds_c.write("\tXGM_stopPlayPCM(SOUND_PCM_CH2);\n")
elif sound_drv == "2ADPCM":
    sounds_c.write("\tSND_stopPlay_2ADPCM(SOUND_PCM_CH2);\n")
    sounds_c.write("\tSND_stopPlay_2ADPCM(SOUND_PCM_CH1);\n")
elif sound_drv == "4PCM":
    sounds_c.write("\tSND_stopPlay_4PCM(SOUND_PCM_CH2);\n")
    
sounds_c.write("}\n\n")

sounds_c.write("void novel_stop_music() {\n")
if sound_drv == "XGM":
    sounds_c.write("\tXGM_stopPlay();\n")
elif sound_drv == "2ADPCM":
    sounds_c.write("\tSND_stopPlay_2ADPCM(SOUND_PCM_CH1);\n")
elif sound_drv == "4PCM":
    sounds_c.write("\tSND_stopPlay_4PCM(SOUND_PCM_CH1);\n")
    
sounds_c.write("}\n\n")


############### MUSIC

if os.path.isdir("res\\music"):
    shutil.rmtree("res\\music")
os.mkdir("res\\music")


have_music = False
if os.path.isdir("novel\\music"):

    if sound_drv == "XGM":
        for music in glob.glob("novel\\music\\**\\*.vgm", recursive=True):
            have_music = True
            music = os.path.basename(music)
            alias = music.replace(".", "_")
            sounds_c.write("void play_music_" + alias + "() {\n")
            sounds_c.write("\tXGM_startPlay_FAR(" + alias + ", sizeof(" + alias + "));\n")
            sounds_c.write("}\n\n")
    elif sound_drv == "2ADPCM" or sound_drv == "4PCM":
        music_num = 0
        for music in glob.glob("novel\\music\\**\\*.wav", recursive=True):
            have_music = True
            music = os.path.basename(music)
            music_num +=1
            alias = "music_" + str(music_num)
            sounds_c.write("void play_" + alias + "() {\n")
            if sound_drv == "2ADPCM":
                sounds_c.write("\tSND_startPlay_2ADPCM(" + alias + ", sizeof(" + alias + "), SOUND_PCM_CH1, 1);\n")
            else:
                sounds_c.write("\tSND_startPlay_4PCM(" + alias + ", sizeof(" + alias + "), SOUND_PCM_CH1, 1);\n")
            sounds_c.write("}\n\n")

if not have_music:
    sounds_c.write("void play_null_music() {}\n")

sounds_c.write("void (*NOVEL_PLAY_MUSIC[])() = {\n")

if os.path.isdir("novel\\music"):

    if sound_drv == "XGM":

        for music in glob.glob("novel\\music\\**\\*.vgm", recursive=True):
            print(music)
            shutil.copyfile(music, music.replace("novel\\music", "res\\music"))
            music = os.path.basename(music)
            alias = music.replace(".", "_")
            sound_res.write("XGM " + alias + " music/" + music + "\n" )
            sounds_c.write("play_music_" + alias + ",\n")
    elif sound_drv == "2ADPCM" or sound_drv == "4PCM":
        music_num = 0
        for music in glob.glob("novel\\music\\**\\*.wav", recursive=True):
            print(music)
            outmusic = music.replace("novel\\music", "res\\music")
            pathlib.Path(os.path.dirname(outmusic)).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(music, outmusic)
            music = outmusic.replace("res\\music\\", "", 1)
            music_num +=1
            alias = "music_" + str(music_num)
            sound_res.write("WAV " + alias + " music/" + music + " " + sound_drv + "\n" )
            sounds_c.write("play_" + alias + ",\n")

if not have_music:
    sounds_c.write("play_null_music\n")
else:
     sound_res.write("\n\n\n")
sounds_c.write("};\n\n")



######################## WAV
wav_files = {}
for wav in glob.glob("novel\\wav\\**\\*.wav", recursive=True):
    wav_files[wav.replace("novel\\", "", 1)] = "wav_" + str(len(wav_files))
    #continue
    outwav = wav.replace("novel\\wav", "res\\wav")
    pathlib.Path(os.path.dirname(outwav)).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(wav, outwav)


have_sounds = False
for wav in wav_files.keys():
    have_sounds = True
    alias = wav_files[wav]
    sounds_c.write("void play_" + alias + "(int v) {\n")

    sound_res.write("WAV " + alias + " " + wav + " " + sound_drv + " \n" )
    
    if sound_drv == "XGM":
        sounds_c.write("\tnovel_stop_sound();\n")
        sounds_c.write("\tSYS_doVBlankProcess();\n")
        sounds_c.write("\tXGM_setPCM(68, FAR_SAFE(&" + alias + ", sizeof("+ alias + "))," + "sizeof("+ alias + "));\n")
        sounds_c.write("\tSYS_doVBlankProcess();\n")
        sounds_c.write("\tXGM_startPlayPCM(68,1,SOUND_PCM_CH2);\n")
    
    elif sound_drv == "2ADPCM":
        #sounds_c.write("\tSND_startPlay_2ADPCM(" + alias + ", sizeof(" + alias + "), SOUND_PCM_CH2, 0);\n")
        #sounds_c.write("\tnovel_stop_sound();\n")
        sounds_c.write("\tSYS_doVBlankProcess();\n")
        sounds_c.write("\tif (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(" + alias + ", sizeof(" + alias + ")), sizeof(" + alias + "), SOUND_PCM_CH2, 0);\n")
        sounds_c.write("\tif (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(" + alias + ", sizeof(" + alias + ")), sizeof(" + alias + "), SOUND_PCM_CH1, 1);\n")
        #sounds_c.write("\tSND_startPlay_2ADPCM( FAR_SAFE(" + alias + ", sizeof(" + alias + ")), sizeof(" + alias + "), SOUND_PCM_CH2, v);\n")
        #sounds_c.write("\tSYS_doVBlankProcess();\n")
    elif sound_drv == "4PCM":
        #sounds_c.write("\tSND_startPlay_4PCM(" + alias + ", sizeof(" + alias + "), SOUND_PCM_CH2, 0);\n")
        sounds_c.write("\tnovel_stop_sound();\n")
        sounds_c.write("\tSYS_doVBlankProcess();\n")
        sounds_c.write("\tSND_startPlay_4PCM( FAR_SAFE(" + alias + ", sizeof(" + alias + ")), sizeof(" + alias + "), SOUND_PCM_CH2, v);\n")
        sounds_c.write("\tSYS_doVBlankProcess();\n")
    else:
        print("---------------------- ERROR --------------------")
        print("  The sound driver is not right in the novel.ini file")
        print("    Use 2ADPCM or XGM")
        print("--------------------------------------------------")
    sounds_c.write("}\n")

if not have_sounds:
    sounds_c.write("void play_null_sound(int v) {}\n")
    
sounds_c.write("void (*NOVEL_PLAY_SOUND[])() = {\n")
for wav in wav_files.keys():
    alias = "play_" + wav_files[wav]
    sounds_c.write(alias + ",\n")
if not have_sounds:
    sounds_c.write("play_null_sound\n")
else:
     sound_res.write("\n\n\n")
sounds_c.write("};\n\n")






