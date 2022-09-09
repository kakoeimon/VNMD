#include "novel_sounds.h"

void novel_stop_sound() {
	SND_stopPlay_2ADPCM(SOUND_PCM_CH2);
	SND_stopPlay_2ADPCM(SOUND_PCM_CH1);
}

void novel_stop_music() {
	SND_stopPlay_2ADPCM(SOUND_PCM_CH1);
}

void play_music_1() {
	SND_startPlay_2ADPCM(music_1, sizeof(music_1), SOUND_PCM_CH1, 1);
}

void play_music_2() {
	SND_startPlay_2ADPCM(music_2, sizeof(music_2), SOUND_PCM_CH1, 1);
}

void play_music_3() {
	SND_startPlay_2ADPCM(music_3, sizeof(music_3), SOUND_PCM_CH1, 1);
}

void play_music_4() {
	SND_startPlay_2ADPCM(music_4, sizeof(music_4), SOUND_PCM_CH1, 1);
}

void play_music_5() {
	SND_startPlay_2ADPCM(music_5, sizeof(music_5), SOUND_PCM_CH1, 1);
}

void play_music_6() {
	SND_startPlay_2ADPCM(music_6, sizeof(music_6), SOUND_PCM_CH1, 1);
}

void play_music_7() {
	SND_startPlay_2ADPCM(music_7, sizeof(music_7), SOUND_PCM_CH1, 1);
}

void play_music_8() {
	SND_startPlay_2ADPCM(music_8, sizeof(music_8), SOUND_PCM_CH1, 1);
}

void play_music_9() {
	SND_startPlay_2ADPCM(music_9, sizeof(music_9), SOUND_PCM_CH1, 1);
}

void play_music_10() {
	SND_startPlay_2ADPCM(music_10, sizeof(music_10), SOUND_PCM_CH1, 1);
}

void play_music_11() {
	SND_startPlay_2ADPCM(music_11, sizeof(music_11), SOUND_PCM_CH1, 1);
}

void play_music_12() {
	SND_startPlay_2ADPCM(music_12, sizeof(music_12), SOUND_PCM_CH1, 1);
}

void play_music_13() {
	SND_startPlay_2ADPCM(music_13, sizeof(music_13), SOUND_PCM_CH1, 1);
}

void (*NOVEL_PLAY_MUSIC[])() = {
play_music_1,
play_music_2,
play_music_3,
play_music_4,
play_music_5,
play_music_6,
play_music_7,
play_music_8,
play_music_9,
play_music_10,
play_music_11,
play_music_12,
play_music_13,
};

void play_wav_0(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_0, sizeof(wav_0)), sizeof(wav_0), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_0, sizeof(wav_0)), sizeof(wav_0), SOUND_PCM_CH1, 1);
}
void play_wav_1(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_1, sizeof(wav_1)), sizeof(wav_1), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_1, sizeof(wav_1)), sizeof(wav_1), SOUND_PCM_CH1, 1);
}
void play_wav_2(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_2, sizeof(wav_2)), sizeof(wav_2), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_2, sizeof(wav_2)), sizeof(wav_2), SOUND_PCM_CH1, 1);
}
void play_wav_3(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_3, sizeof(wav_3)), sizeof(wav_3), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_3, sizeof(wav_3)), sizeof(wav_3), SOUND_PCM_CH1, 1);
}
void play_wav_4(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_4, sizeof(wav_4)), sizeof(wav_4), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_4, sizeof(wav_4)), sizeof(wav_4), SOUND_PCM_CH1, 1);
}
void play_wav_5(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_5, sizeof(wav_5)), sizeof(wav_5), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_5, sizeof(wav_5)), sizeof(wav_5), SOUND_PCM_CH1, 1);
}
void play_wav_6(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_6, sizeof(wav_6)), sizeof(wav_6), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_6, sizeof(wav_6)), sizeof(wav_6), SOUND_PCM_CH1, 1);
}
void play_wav_7(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_7, sizeof(wav_7)), sizeof(wav_7), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_7, sizeof(wav_7)), sizeof(wav_7), SOUND_PCM_CH1, 1);
}
void play_wav_8(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_8, sizeof(wav_8)), sizeof(wav_8), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_8, sizeof(wav_8)), sizeof(wav_8), SOUND_PCM_CH1, 1);
}
void play_wav_9(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_9, sizeof(wav_9)), sizeof(wav_9), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_9, sizeof(wav_9)), sizeof(wav_9), SOUND_PCM_CH1, 1);
}
void play_wav_10(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_10, sizeof(wav_10)), sizeof(wav_10), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_10, sizeof(wav_10)), sizeof(wav_10), SOUND_PCM_CH1, 1);
}
void play_wav_11(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_11, sizeof(wav_11)), sizeof(wav_11), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_11, sizeof(wav_11)), sizeof(wav_11), SOUND_PCM_CH1, 1);
}
void play_wav_12(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_12, sizeof(wav_12)), sizeof(wav_12), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_12, sizeof(wav_12)), sizeof(wav_12), SOUND_PCM_CH1, 1);
}
void play_wav_13(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_13, sizeof(wav_13)), sizeof(wav_13), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_13, sizeof(wav_13)), sizeof(wav_13), SOUND_PCM_CH1, 1);
}
void play_wav_14(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_14, sizeof(wav_14)), sizeof(wav_14), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_14, sizeof(wav_14)), sizeof(wav_14), SOUND_PCM_CH1, 1);
}
void play_wav_15(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_15, sizeof(wav_15)), sizeof(wav_15), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_15, sizeof(wav_15)), sizeof(wav_15), SOUND_PCM_CH1, 1);
}
void play_wav_16(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_16, sizeof(wav_16)), sizeof(wav_16), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_16, sizeof(wav_16)), sizeof(wav_16), SOUND_PCM_CH1, 1);
}
void play_wav_17(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_17, sizeof(wav_17)), sizeof(wav_17), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_17, sizeof(wav_17)), sizeof(wav_17), SOUND_PCM_CH1, 1);
}
void play_wav_18(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_18, sizeof(wav_18)), sizeof(wav_18), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_18, sizeof(wav_18)), sizeof(wav_18), SOUND_PCM_CH1, 1);
}
void play_wav_19(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_19, sizeof(wav_19)), sizeof(wav_19), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_19, sizeof(wav_19)), sizeof(wav_19), SOUND_PCM_CH1, 1);
}
void play_wav_20(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_20, sizeof(wav_20)), sizeof(wav_20), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_20, sizeof(wav_20)), sizeof(wav_20), SOUND_PCM_CH1, 1);
}
void play_wav_21(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_21, sizeof(wav_21)), sizeof(wav_21), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_21, sizeof(wav_21)), sizeof(wav_21), SOUND_PCM_CH1, 1);
}
void play_wav_22(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_22, sizeof(wav_22)), sizeof(wav_22), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_22, sizeof(wav_22)), sizeof(wav_22), SOUND_PCM_CH1, 1);
}
void play_wav_23(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_23, sizeof(wav_23)), sizeof(wav_23), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_23, sizeof(wav_23)), sizeof(wav_23), SOUND_PCM_CH1, 1);
}
void play_wav_24(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_24, sizeof(wav_24)), sizeof(wav_24), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_24, sizeof(wav_24)), sizeof(wav_24), SOUND_PCM_CH1, 1);
}
void play_wav_25(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_25, sizeof(wav_25)), sizeof(wav_25), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_25, sizeof(wav_25)), sizeof(wav_25), SOUND_PCM_CH1, 1);
}
void play_wav_26(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_26, sizeof(wav_26)), sizeof(wav_26), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_26, sizeof(wav_26)), sizeof(wav_26), SOUND_PCM_CH1, 1);
}
void play_wav_27(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_27, sizeof(wav_27)), sizeof(wav_27), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_27, sizeof(wav_27)), sizeof(wav_27), SOUND_PCM_CH1, 1);
}
void play_wav_28(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_28, sizeof(wav_28)), sizeof(wav_28), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_28, sizeof(wav_28)), sizeof(wav_28), SOUND_PCM_CH1, 1);
}
void play_wav_29(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_29, sizeof(wav_29)), sizeof(wav_29), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_29, sizeof(wav_29)), sizeof(wav_29), SOUND_PCM_CH1, 1);
}
void play_wav_30(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_30, sizeof(wav_30)), sizeof(wav_30), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_30, sizeof(wav_30)), sizeof(wav_30), SOUND_PCM_CH1, 1);
}
void play_wav_31(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_31, sizeof(wav_31)), sizeof(wav_31), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_31, sizeof(wav_31)), sizeof(wav_31), SOUND_PCM_CH1, 1);
}
void play_wav_32(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_32, sizeof(wav_32)), sizeof(wav_32), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_32, sizeof(wav_32)), sizeof(wav_32), SOUND_PCM_CH1, 1);
}
void play_wav_33(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_33, sizeof(wav_33)), sizeof(wav_33), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_33, sizeof(wav_33)), sizeof(wav_33), SOUND_PCM_CH1, 1);
}
void play_wav_34(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_34, sizeof(wav_34)), sizeof(wav_34), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_34, sizeof(wav_34)), sizeof(wav_34), SOUND_PCM_CH1, 1);
}
void play_wav_35(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_35, sizeof(wav_35)), sizeof(wav_35), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_35, sizeof(wav_35)), sizeof(wav_35), SOUND_PCM_CH1, 1);
}
void play_wav_36(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_36, sizeof(wav_36)), sizeof(wav_36), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_36, sizeof(wav_36)), sizeof(wav_36), SOUND_PCM_CH1, 1);
}
void play_wav_37(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_37, sizeof(wav_37)), sizeof(wav_37), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_37, sizeof(wav_37)), sizeof(wav_37), SOUND_PCM_CH1, 1);
}
void play_wav_38(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_38, sizeof(wav_38)), sizeof(wav_38), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_38, sizeof(wav_38)), sizeof(wav_38), SOUND_PCM_CH1, 1);
}
void play_wav_39(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_39, sizeof(wav_39)), sizeof(wav_39), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_39, sizeof(wav_39)), sizeof(wav_39), SOUND_PCM_CH1, 1);
}
void play_wav_40(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_40, sizeof(wav_40)), sizeof(wav_40), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_40, sizeof(wav_40)), sizeof(wav_40), SOUND_PCM_CH1, 1);
}
void play_wav_41(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_41, sizeof(wav_41)), sizeof(wav_41), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_41, sizeof(wav_41)), sizeof(wav_41), SOUND_PCM_CH1, 1);
}
void play_wav_42(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_42, sizeof(wav_42)), sizeof(wav_42), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_42, sizeof(wav_42)), sizeof(wav_42), SOUND_PCM_CH1, 1);
}
void play_wav_43(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_43, sizeof(wav_43)), sizeof(wav_43), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_43, sizeof(wav_43)), sizeof(wav_43), SOUND_PCM_CH1, 1);
}
void play_wav_44(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_44, sizeof(wav_44)), sizeof(wav_44), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_44, sizeof(wav_44)), sizeof(wav_44), SOUND_PCM_CH1, 1);
}
void play_wav_45(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_45, sizeof(wav_45)), sizeof(wav_45), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_45, sizeof(wav_45)), sizeof(wav_45), SOUND_PCM_CH1, 1);
}
void play_wav_46(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_46, sizeof(wav_46)), sizeof(wav_46), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_46, sizeof(wav_46)), sizeof(wav_46), SOUND_PCM_CH1, 1);
}
void play_wav_47(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_47, sizeof(wav_47)), sizeof(wav_47), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_47, sizeof(wav_47)), sizeof(wav_47), SOUND_PCM_CH1, 1);
}
void play_wav_48(int v) {
	SYS_doVBlankProcess();
	if (v != 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_48, sizeof(wav_48)), sizeof(wav_48), SOUND_PCM_CH2, 0);
	if (v == 1) SND_startPlay_2ADPCM( FAR_SAFE(wav_48, sizeof(wav_48)), sizeof(wav_48), SOUND_PCM_CH1, 1);
}
void (*NOVEL_PLAY_SOUND[])() = {
play_wav_0,
play_wav_1,
play_wav_2,
play_wav_3,
play_wav_4,
play_wav_5,
play_wav_6,
play_wav_7,
play_wav_8,
play_wav_9,
play_wav_10,
play_wav_11,
play_wav_12,
play_wav_13,
play_wav_14,
play_wav_15,
play_wav_16,
play_wav_17,
play_wav_18,
play_wav_19,
play_wav_20,
play_wav_21,
play_wav_22,
play_wav_23,
play_wav_24,
play_wav_25,
play_wav_26,
play_wav_27,
play_wav_28,
play_wav_29,
play_wav_30,
play_wav_31,
play_wav_32,
play_wav_33,
play_wav_34,
play_wav_35,
play_wav_36,
play_wav_37,
play_wav_38,
play_wav_39,
play_wav_40,
play_wav_41,
play_wav_42,
play_wav_43,
play_wav_44,
play_wav_45,
play_wav_46,
play_wav_47,
play_wav_48,
};

