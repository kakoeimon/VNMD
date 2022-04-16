#ifndef H_NOVEL_FUNCTIONS
#define H_NOVEL_FUNCTIONS

#include "genesis.h"
#define NONOT 16000

extern s32 NOVEL_POSITION;
extern u16 NOVEL_SCR_INDEX;
extern int NOVEL_BACK_INDEX;
extern int NOVEL_FORE_INDEX;
extern int NOVEL_FORE_IMGS[3];
extern int NOVEL_FORE_IMGS_POS[3][2];

extern int NOVEL_SELECTED;
extern int NOVEL_ADVANCE;

extern int NOVEL_PAUSE_MENU;

extern int NOVEL_INTERAPTED;



void draw_int(int value, int x, int y);

void draw_background(int index, int fade_time);
void draw_foreground(int index, int x, int y);
int draw_text(char *str);


#endif