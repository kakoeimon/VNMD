#include "novel_sounds.h"

void novel_stop_sound() {
	XGM_stopPlayPCM(SOUND_PCM_CH2);
}

void novel_stop_music() {
	XGM_stopPlay();
}

void play_null_music() {}
void (*NOVEL_PLAY_MUSIC[])() = {
play_null_music
};

void play_null_sound(int v) {}
void (*NOVEL_PLAY_SOUND[])() = {
play_null_sound
};

