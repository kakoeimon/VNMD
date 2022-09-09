#ifndef H_NOVEL_SOUNDS
#define H_NOVEL_SOUNDS

#include "genesis.h"
#include "novel_sounds_res.h"

extern void (*NOVEL_PLAY_SOUND[])(int v);
extern void (*NOVEL_PLAY_MUSIC[])();

void novel_stop_sound();

void novel_stop_music();

#endif