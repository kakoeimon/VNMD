#include "novel_functions.h"
#include "novel_scripts.h"
#include "novel_images.h"
#include "novel_variables.h"

#define NOVEL_FORE_PAL_START 1

Novel NOVEL;

void draw_int(int value, int x, int y) {
    char str[4];
    intToStr(value, str, 4);
    VDP_drawText(str, x, y);
}

void clear_text() {
    //static s16 novel_text_height = NOVEL_TEXT_BOTTOM - NOVEL_TEXT_TOP;
    VDP_clearPlane(WINDOW, TRUE);
    //VDP_clearTextArea(NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP, NOVEL_TEXT_WIDTH, novel_text_height);
}

void novel_draw_background(int index, int fade_time) {
    const Image *img = NOVEL_BACKGROUND[index];
    
    //VDP_clearPlane(BG_B, FALSE);
    
    
    NOVEL.fore_pal = NOVEL_FORE_PAL_START;
    NOVEL.fore_index = TILE_USER_INDEX + img->tileset->numTile;
    for (int i = 0; i < 3; i++) {
        NOVEL.fore_imgs[i] = MAX_S16;
    }
    VDP_clearPlane(BG_A, TRUE);
    SYS_doVBlankProcess();
    
    SYS_doVBlankProcess();
    if (index != NOVEL.back_index) {
        
        SYS_doVBlankProcess();
        SYS_doVBlankProcess();
        //PAL_setPalette(PAL0, palette_black, CPU);

        VDP_loadTileSet(img->tileset,TILE_USER_INDEX, DMA_QUEUE);
        
        //for (int i =0; i < 60; i++) SYS_doVBlankProcess();


        NOVEL.back_index = index;
        VDP_setTileMapEx(BG_B, img->tilemap, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, TILE_USER_INDEX), NOVEL_BG_LEFT, NOVEL_BG_TOP,  0, 0, NOVEL_BG_WIDTH, NOVEL_BG_HEIGHT, DMA_QUEUE);
        PAL_setPalette(PAL0, img->palette->data, DMA_QUEUE);
        SYS_doVBlankProcess();
    }

    for (int i = 0; i < fade_time; i++) {

        SYS_doVBlankProcess();
        if (NOVEL.advance) {
            break;
        }
    }
    SYS_doVBlankProcess();
    SYS_doVBlankProcess();
    
}

void novel_draw_foreground(int index, int x, int y) {
    const Image *img = NOVEL_FOREGROUND[index];
    int s_x = img->tilemap->w;
    int s_y = img->tilemap->h;
    SYS_doVBlankProcess();
    VDP_loadTileSet(img->tileset,NOVEL.fore_index, DMA_QUEUE);
    SYS_doVBlankProcess();
    PAL_setPalette(NOVEL.fore_pal, img->palette->data, DMA_QUEUE);
    SYS_doVBlankProcess();
    VDP_setTileMapEx(BG_A, img->tilemap, TILE_ATTR_FULL(NOVEL.fore_pal, FALSE, FALSE, FALSE, NOVEL.fore_index), x, y,  0, 0, s_x, s_y, DMA_QUEUE);
    //those 3 FORE IMGS are for the save function
    NOVEL.fore_imgs[NOVEL.fore_pal-1] = index;
    NOVEL.fore_pos[NOVEL.fore_pal-1][0] = x;
    NOVEL.fore_pos[NOVEL.fore_pal-1][1] = y;
    NOVEL.fore_pal++;
    if (NOVEL.fore_pal > 3) {
        NOVEL.fore_pal = NOVEL_FORE_PAL_START;
    }
    NOVEL.fore_index += img->tileset->numTile;
    //VDP_loadFont(&font_default, DMA);
    SYS_doVBlankProcess();
}


int draw_line(char *str, int draw_pos) {
    u8 line[NOVEL_TEXT_WIDTH];
    int wanted_length = NOVEL_TEXT_WIDTH;
    if (strlen(str) > NOVEL_TEXT_WIDTH) {
        while( str[wanted_length] != ' ' && wanted_length != 0) {
            wanted_length--;
        }
        if (wanted_length == 0) {
            wanted_length = NOVEL_TEXT_WIDTH;
        }
    }
    strncpy(line, str, wanted_length++);
    
    VDP_drawText(line, NOVEL_TEXT_LEFT, draw_pos);
    

    if (draw_pos >= NOVEL_TEXT_BOTTOM - 1 || strlen(str) <= NOVEL_TEXT_WIDTH) {
        draw_pos = NOVEL_TEXT_TOP - 1;
        SYS_doVBlankProcess();
        if (NOVEL.pause_menu) return 0;
        
        while (NOVEL.advance != TRUE)
        {
            
            SYS_doVBlankProcess();
            if (NOVEL.pause_menu) return 0;
            u16 joy = JOY_readJoypad(JOY_1);
            if (joy & BUTTON_C) {
                NOVEL.advance = TRUE;
            }
        }
        NOVEL.advance = FALSE;
        NOVEL.selected = FALSE;
        clear_text();
    }
    if (strlen(str) > NOVEL_TEXT_WIDTH) {
        return draw_line(&str[wanted_length], draw_pos+1);
    }
    return 1;
}

int draw_text(char *str) {
    if (str[0] == '@' || str[0] == '!' || str[0] == '~') {
        int draw_pos = NOVEL_TEXT_TOP - 1;
        if (str[0] == '!') {
            char tmp_str[NOVEL_TEXT_WIDTH];
            for (int i = 0; i < NOVEL_TEXT_WIDTH; i++) {
                tmp_str[i] = ' ';
            }
            tmp_str[NOVEL_TEXT_WIDTH-2] = '!';
            if (!draw_line(tmp_str, NOVEL_TEXT_BOTTOM - 2)) {
                return 0;
            }
        } else {
            if (!draw_line(str+1, NOVEL_TEXT_TOP)) {
                return 0;
            }
        }
        
    } else if (!draw_line(str, NOVEL_TEXT_TOP)) {
        return 0;
    }
    return strlen(str) + 2;
     
}
