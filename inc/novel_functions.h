#ifndef H_NOVEL_FUNCTIONS
#define H_NOVEL_FUNCTIONS

#include "genesis.h"


typedef struct Novel_ {
    s32 position;
    u16 script_index;
    s16 back_index;
    s16 fore_index;
    s16 fore_pal;
    s16 selected;
    s16 advance;
    s16 pause_menu;
    s16 pause_menu_pos;
    s16 pause_menu_selected;
    s16 fore_imgs[3];
    s16 fore_pos[3][2];
} Novel;

extern Novel NOVEL;

void draw_int(int value, int x, int y);

void draw_background(int index, int fade_time);
void draw_foreground(int index, int x, int y);
int draw_text(char *str);


#endif