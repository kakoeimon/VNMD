#include "novel_functions.h"
#include "novel_scripts.h"
#include "novel_images.h"
#include "novel_variables.h"

#define NOVEL_FORE_PAL_START 1

s32 NOVEL_POSITION = 0;
u16 NOVEL_SCR_INDEX = 0;
int NOVEL_BACK_INDEX = -1;
int NOVEL_FORE_INDEX = -1;

int NOVEL_FORE_IMGS[3] = {MAX_S16, MAX_S16, MAX_S16};
int NOVEL_FORE_IMGS_POS[3][2] = {{0,0}, {0,0}, {0,0}};

int NOVEL_SELECTED = FALSE;
int NOVEL_ADVANCE = FALSE;

int NOVEL_PAUSE_MENU = FALSE;

int NOVEL_INTERAPTED = FALSE;

int NOVEL_FORE_PAL = NOVEL_FORE_PAL_START;

void draw_int(int value, int x, int y) {
    char str[4];
    intToStr(value, str, 4);
    VDP_drawText(str, x, y);
}

void draw_background(int index, int fade_time) {
    const Image *img = NOVEL_BACKGROUND[index];
    
    //VDP_clearPlane(BG_B, FALSE);
    VDP_clearPlane(BG_A, FALSE);
    NOVEL_FORE_PAL = NOVEL_FORE_PAL_START;
    NOVEL_FORE_INDEX = TILE_USERINDEX + img->tileset->numTile;
    for (int i = 0; i < 3; i++) {
        NOVEL_FORE_IMGS[i] = MAX_S16;
    }
    SYS_doVBlankProcess();
    SYS_doVBlankProcess();
    if (index != NOVEL_BACK_INDEX) {
        SYS_doVBlankProcess();
        SYS_doVBlankProcess();
        //PAL_setPalette(PAL0, palette_black, DMA);
        VDP_loadTileSet(img->tileset,TILE_USERINDEX, DMA_QUEUE);
        NOVEL_BACK_INDEX = index;
        //SYS_doVBlankProcess();
        
        
        VDP_setTileMapEx(BG_B, img->tilemap, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, TILE_USERINDEX), NOVEL_BG_LEFT, NOVEL_BG_TOP,  0, 0, NOVEL_BG_WIDTH, NOVEL_BG_HEIGHT, DMA_QUEUE);
        PAL_setPalette(PAL0, img->palette->data, DMA_QUEUE);
        
        
        SYS_doVBlankProcess();
    }

    for (int i = 0; i < fade_time; i++) {

        SYS_doVBlankProcess();
        if (NOVEL_ADVANCE) {
            break;
        }
    }
    SYS_doVBlankProcess();
    SYS_doVBlankProcess();
    
}

void draw_foreground(int index, int x, int y) {
    const Image *img = NOVEL_FOREGROUND[index];
    int s_x = NOVEL_FOREGROUND_SIZE[index][0];
    int s_y = NOVEL_FOREGROUND_SIZE[index][1];
    
    VDP_loadTileSet(img->tileset,NOVEL_FORE_INDEX, DMA_QUEUE);
    SYS_doVBlankProcess();
    PAL_setPalette(NOVEL_FORE_PAL, img->palette->data, DMA_QUEUE);
    SYS_doVBlankProcess();
    VDP_setTileMapEx(BG_A, img->tilemap, TILE_ATTR_FULL(NOVEL_FORE_PAL, FALSE, FALSE, FALSE, NOVEL_FORE_INDEX), x, y,  0, 0, s_x, s_y, DMA_QUEUE);
    //those 3 FORE IMGS are for the save function
    NOVEL_FORE_IMGS[NOVEL_FORE_PAL-1] = index;
    NOVEL_FORE_IMGS_POS[NOVEL_FORE_PAL-1][0] = x;
    NOVEL_FORE_IMGS_POS[NOVEL_FORE_PAL-1][1] = y;
    NOVEL_FORE_PAL++;
    if (NOVEL_FORE_PAL > 3) {
        NOVEL_FORE_PAL = NOVEL_FORE_PAL_START;
    }
    NOVEL_FORE_INDEX += img->tileset->numTile;
    SYS_doVBlankProcess();
}


int draw_line(char *str, int draw_pos) {
    NOVEL_INTERAPTED = FALSE;
    u8 line[NOVEL_TEXT_WIDTH];
    int wanted_length = NOVEL_TEXT_WIDTH;
    if (strlen(str) > NOVEL_TEXT_WIDTH) {
        while( str[wanted_length] != ' ') {
            wanted_length--;
        }
    }
    strncpy(line, str, wanted_length++);
    if (line[0] == '@' || line[0] == '!' || line[0] == '~') {
        VDP_drawText(&line[1], NOVEL_TEXT_LEFT, draw_pos);
    } else {
        VDP_drawText(line, NOVEL_TEXT_LEFT, draw_pos);
    }

    if (draw_pos >= NOVEL_TEXT_BOTTOM - 1 || strlen(str) <= NOVEL_TEXT_WIDTH) {
        draw_pos = NOVEL_TEXT_TOP - 1;
        SYS_doVBlankProcess();
        if (NOVEL_INTERAPTED) return 0;
        
        while (NOVEL_ADVANCE != TRUE)
        {
            
            SYS_doVBlankProcess();
            if (NOVEL_INTERAPTED) return 0;
            u16 joy = JOY_readJoypad(JOY_1);
            if (joy & BUTTON_C) {
                NOVEL_ADVANCE = TRUE;
            }
        }
        NOVEL_ADVANCE = FALSE;
        NOVEL_SELECTED = FALSE;
        clear_text();
    }
    if (strlen(str) > NOVEL_TEXT_WIDTH) {
        return draw_line(&str[wanted_length], draw_pos+1);
    }
    return 1;
}

int draw_text(char *str) {
    if (!draw_line(str, NOVEL_TEXT_TOP)) {
        return 0;
    }
    return strlen(str) + 2;
     
}
