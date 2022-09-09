#include "genesis.h"
#include "novel_player.h"
#include "novel_functions.h"
#include "novel_scripts.h"
#include "novel_images.h"
#include "novel_sounds.h"
#include "novel_variables.h"

char NOVEL_CHOICE_CHAR[1] = {'z' + 5};

int NOVEL_ACTUAL_TEXT_TOP = NOVEL_TEXT_TOP;

int bytes_to_int(int byte1, int byte2) {
    return byte2 | byte1 << 8;
}


u8 *get_pos() {
    return FAR_SAFE(NOVEL_SCRIPTS[NOVEL.script_index]+NOVEL.position, NOVEL_SCRIPTS_BYTES_COUNT[NOVEL.script_index]);
}

u8 read_char() {
    u8 r = *get_pos();
    NOVEL.position++;
    return r;
}

int read_int() {
    u8 a = *get_pos();
    NOVEL.position++;
    u8 b = *get_pos();
    NOVEL.position++;
    return b | a << 8;
}


u16 read_u16() {
    u8 a = *get_pos();
    NOVEL.position++;
    u8 b = *get_pos();
    NOVEL.position++;
    return b | a << 8;
}


s32 read_s32() {
    u8 a = *get_pos();
    NOVEL.position++;
    u8 b = *get_pos();
    NOVEL.position++;
    u8 c = *get_pos();
    NOVEL.position++;
    u8 d = *get_pos();
    NOVEL.position++;
    //long result = (((bytes[0] << 8 & bytes[1]) << 8 & bytes[2]) << 8) & bytes[3]
    return d | c << 8 | b << 16 | a << 24;;
}


void novel_event_handler(u16 joy, u16 changed, u16 state) {
    if (joy == JOY_1) {
        if (state & changed & BUTTON_A || state & changed & BUTTON_C) {
            NOVEL.advance = TRUE;
        } else if (state & changed & BUTTON_START) {
            NOVEL.pause_menu = TRUE;
        }
    }
}

void novel_choice_event_handler(u16 joy, u16 changed, u16 state) {
    if (state & changed & BUTTON_UP) {
        NOVEL_VARIABLES[0] -= 1;
    } else if (state & changed & BUTTON_DOWN) {
        NOVEL_VARIABLES[0] += 1;
    } else if (state & changed & BUTTON_LEFT) {
        NOVEL_VARIABLES[0] -= NOVEL_TEXT_BOTTOM - NOVEL_ACTUAL_TEXT_TOP;
    } else if (state & changed & BUTTON_RIGHT) {
        NOVEL_VARIABLES[0] += NOVEL_TEXT_BOTTOM - NOVEL_ACTUAL_TEXT_TOP;
    } else if (state & changed & BUTTON_B) {
        NOVEL.selected = TRUE;
    } else if (state & changed & BUTTON_START) {
        NOVEL.pause_menu = TRUE;
    }
}


void novel_set_bg_palette() {
    PAL_setPalette(PAL0, NOVEL_BACKGROUND[NOVEL.back_index]->palette->data, CPU);
}


void novel_pause_event_handler(u16 joy, u16 changed, u16 state) {
    if (state & changed & BUTTON_UP) {
        NOVEL.pause_menu_pos -= 1;
    } else if (state & changed & BUTTON_DOWN) {
        NOVEL.pause_menu_pos += 1;
    }  else if (state & changed & BUTTON_B) {
        NOVEL.pause_menu_selected = TRUE;
    } else if (state & changed & BUTTON_START) {
        NOVEL.pause_menu = FALSE;
    }
}

void novel_pause_menu_set_cursor(int max_values) {
    for (int i = 0; i < 3; i++) {
        VDP_clearText(NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + i, 1);
    }
        if (NOVEL.pause_menu_pos < 0) NOVEL.pause_menu_pos = max_values - 1;
        if (NOVEL.pause_menu_pos >= max_values) NOVEL.pause_menu_pos = 0;
        VDP_drawText(NOVEL_CHOICE_CHAR, NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + NOVEL.pause_menu_pos);
}

int novel_get_save_index() {
    int base_length = 4 + NOVEL_NUM_GLOBAL_VARIABLES * 2;
    int save_length = (NOVEL_NUM_VARIABLES * 2 + 2 + 2 + 6 * 3 + 4 + 2 + 2) * (NOVEL.pause_menu_pos + 1);
    
    return base_length + save_length;
}

void novel_save() {
    int index = novel_get_save_index();
    
    //draw_int(index, 2, 29); //I have no idea why, but if I delete this line the game crashes.
    clear_text();
    SYS_doVBlankProcess();
    VDP_drawText("Game Saved", NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP);
    SYS_doVBlankProcess();
    SRAM_enable();
    SRAM_writeWord(index, NOVEL_SAVE_CHECK_NUM);
    index +=2;
    SRAM_writeLong(index, NOVEL.position);
    index +=4;
    SRAM_writeWord(index, NOVEL.script_index);
    index += 2;
    SRAM_writeWord(index, NOVEL.back_index);
    index +=2;
    for (int i = 0; i < 3; i++) {
        SRAM_writeWord(index, NOVEL.fore_imgs[i]);
        index +=2;
        SRAM_writeWord(index, NOVEL.fore_pos[i][0]);
        index +=2;
        SRAM_writeWord(index, NOVEL.fore_pos[i][1]);
        index +=2;
    }
    SRAM_writeWord(index, NOVEL.music);
    index +=2;
    
    for (int i = 0; i < NOVEL_NUM_VARIABLES; i++) {
        SRAM_writeWord(index + i*2, NOVEL_VARIABLES[i]);
    }

    SRAM_disable();
    
    for (int i = 0; i < 60; i++) {
        SYS_doVBlankProcess();
    }
    
}

void novel_load() {
    novel_stop_music();
    novel_stop_sound();
    SYS_doVBlankProcess();
    int index = novel_get_save_index();

    //draw_int(index, 2, 29); //I have no idea why, but if I delete this line the game crashes.
    clear_text();
    SYS_doVBlankProcess();
    VDP_drawText("Loading...", NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP);
    SYS_doVBlankProcess();
    SRAM_enable();
    if (NOVEL_SAVE_CHECK_NUM == SRAM_readWord(index)) {
        int tmp_img[3];
        index +=2;
        NOVEL.position = SRAM_readLong(index);
        index +=4;
        NOVEL.script_index = SRAM_readWord(index);
        index += 2;
        int tmp_bg = SRAM_readWord(index);
        index +=2;
        for (int i = 0; i < 3; i++) {
            tmp_img[i] = SRAM_readWord(index);
            index +=2;
            NOVEL.fore_pos[i][0] = SRAM_readWord(index);
            index +=2;
             NOVEL.fore_pos[i][1] = SRAM_readWord(index);
            index +=2;
        }
        NOVEL.music = SRAM_readWord(index);
        index +=2;

        for (int i = 0; i < NOVEL_NUM_VARIABLES; i++) {
            NOVEL_VARIABLES[i] = SRAM_readWord(index + i*2);
        }
        SRAM_disable();

        draw_background(tmp_bg, 16);
        for (int i = 0; i < 3; i++) {
            if (tmp_img[i] != MAX_S16) {
                draw_foreground(tmp_img[i], NOVEL.fore_pos[i][0], NOVEL.fore_pos[i][1]);
            }
        }
        if (NOVEL.music != NOVEL_NO_MUSIC) {
            NOVEL_PLAY_MUSIC[NOVEL.music]();
        } else {
            novel_stop_music();
        }
        NOVEL.pause_menu = FALSE;
        
    } else {
        SRAM_disable();
        VDP_drawText("Empty Slot", NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP);
        for (int i = 0; i < 60; i++) {
            SYS_doVBlankProcess();
        }
    }
    
}


void novel_pause_menu() {
    if (NOVEL.pause_menu) {
        //Stoping all sounds to protect z80
        novel_stop_music();
        novel_stop_sound();
        SYS_doVBlankProcess();

        JOY_setEventHandler(novel_pause_event_handler);
        NOVEL.pause_menu_pos = 0;
        NOVEL.pause_menu_selected = FALSE;
        
        //VDP_clearPlane(WINDOW, TRUE);
        clear_text();
        SYS_doVBlankProcess();
        VDP_drawText("Save", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
        VDP_drawText("Load", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
        VDP_drawText("Return to title Screen", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);

        NOVEL.pause_menu_selected = FALSE;
        while (!NOVEL.pause_menu_selected && NOVEL.pause_menu)
        {   
            
            novel_pause_menu_set_cursor(3);
            SYS_doVBlankProcess();
        }
        SYS_doVBlankProcess();
        if (NOVEL.pause_menu_selected) { 
            NOVEL.pause_menu_selected = FALSE;
            if (NOVEL.pause_menu_pos == 0) {
                clear_text();

                VDP_drawText("Save Slot 1", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
                VDP_drawText("Save Slot 2", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
                VDP_drawText("Save Slot 3", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);
                NOVEL.pause_menu_selected = FALSE;
                while (!NOVEL.pause_menu_selected && NOVEL.pause_menu) {
                    novel_pause_menu_set_cursor(3);
                    SYS_doVBlankProcess();
                }
                if (NOVEL.pause_menu_selected) {
                    SYS_doVBlankProcess();
                    novel_save();
                }
                NOVEL.pause_menu = FALSE;
                if (NOVEL.music != NOVEL_NO_MUSIC) NOVEL_PLAY_MUSIC[NOVEL.music]();
            } else if (NOVEL.pause_menu_pos == 1) {
                NOVEL.pause_menu_pos = 0;
                clear_text();
                
                VDP_drawText("Load Slot 1", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
                VDP_drawText("Load Slot 2", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
                VDP_drawText("Load Slot 3", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);
                NOVEL.pause_menu_selected = FALSE;
                while (!NOVEL.pause_menu_selected && NOVEL.pause_menu) {
                    novel_pause_menu_set_cursor(3);
                    SYS_doVBlankProcess();
                }
                if (NOVEL.pause_menu_selected) {
                    novel_load();
                }
            } else if (NOVEL.pause_menu_pos == 2) {
                NOVEL.pause_menu = FALSE;
                novel_reset(); //Just reset global save will be done only when th novel reach the end
                //novel_save_n_restart(); //Just for testing the global vars
            }
        }
        
        //VDP_clearTextArea(NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP, NOVEL_TEXT_WIDTH, NOVEL_TEXT_BOTTOM - NOVEL_TEXT_TOP);
        NOVEL.pause_menu = FALSE;
        if (NOVEL.music != NOVEL_NO_MUSIC) NOVEL_PLAY_MUSIC[NOVEL.music]();
        clear_text();
        JOY_setEventHandler(novel_event_handler);
    }
    
}

void novel_load_global() {
    //
    //First 2 bytes are the NOVEL_CHECK_NUM
    //NEXT 2 are the NOVEL_NUM_GLOBAL_VARIABLES
    //Those two are checked cause if NOVEL_NUM_GLOBAL_VARIABLES is changed then the global save will be wrong
    // and if the NOVEL_CHECK_NUM is changed the it is another novel.
    //NOVEL_CHECK_NUM is used to easily reset the global save when in development.
    //The first of NOVEL_VARIABLES is the selected
    //
    SYS_doVBlankProcess();
    SRAM_enable();
    if (SRAM_readWord(0) != NOVEL_SAVE_CHECK_NUM || SRAM_readWord(2) != NOVEL_NUM_GLOBAL_VARIABLES) {
        SRAM_writeWord(0, NOVEL_SAVE_CHECK_NUM);
        SRAM_writeWord(2, NOVEL_NUM_GLOBAL_VARIABLES);
        for (int i = 0; i < NOVEL_NUM_GLOBAL_VARIABLES; i++) {
            SRAM_writeWord(i * 2 + 4, 0);
        }
    } else {
        for (int i = 0; i < NOVEL_NUM_GLOBAL_VARIABLES; i++) {
            NOVEL_VARIABLES[i + 1] = SRAM_readWord(i*2+4);
        }
    }
    SRAM_disable();
    SYS_doVBlankProcess();
    
}

void novel_global_save() {
    SYS_doVBlankProcess();
    SRAM_enable();
    for (int i = 0; i < NOVEL_NUM_GLOBAL_VARIABLES; i++) {
        SRAM_writeWord(i*2 + 4, NOVEL_VARIABLES[i + 1]);
    }
    SRAM_disable();
    SYS_doVBlankProcess();
}

void novel_save_n_restart() {
    novel_global_save();
    novel_reset();    
}

void novel_reset_vars() {
    for(int i = 0; i < NOVEL_NUM_VARIABLES; i++) {
        NOVEL_VARIABLES[i] = 0;
    }
    novel_load_global();
}

void novel_reset() {
    NOVEL.position = 0;
    NOVEL.script_index = 0;
    NOVEL.back_index = 1;
    NOVEL.music = NOVEL_NO_MUSIC;
    
    NOVEL.fore_pal = 1;

    VDP_setTextPalette(PAL1);
    PAL_setColor(31, RGB24_TO_VDPCOLOR(0xffffff));
    for (int i = 0; i < 3; i++) {
        NOVEL.fore_imgs[i] = MAX_S16;
    }
    
    NOVEL.selected = 0;
    //NOVEL.script_index = 0;
    NOVEL.advance = FALSE;
    NOVEL.pause_menu = FALSE;


    JOY_setEventHandler(novel_event_handler);

    VDP_setWindowVPos(TRUE, NOVEL_TEXT_TOP);
    
    VDP_setTextPlane(WINDOW);

    novel_reset_vars();
    novel_stop_music();
    clear_text();
    VDP_clearPlane(BG_A, TRUE);
    SYS_doVBlankProcess();
    VDP_clearPlane(BG_B, TRUE);
    SYS_doVBlankProcess();
}


int make_choice(const char *bin) {
    int count = 2;
    NOVEL_VARIABLES[0] = 0;
    int number_of_choices = bin[0];
    NOVEL_ACTUAL_TEXT_TOP = NOVEL_TEXT_TOP;
    int double_row_start = NOVEL_TEXT_BOTTOM - NOVEL_ACTUAL_TEXT_TOP;
    bin++;
    int new_lines = (number_of_choices - double_row_start * 2) / 2 + number_of_choices % 2;
    if (new_lines < 0) new_lines = 0;
    if (new_lines) {
        double_row_start  += new_lines;
        NOVEL_ACTUAL_TEXT_TOP -= new_lines;
        VDP_setWindowVPos(TRUE, NOVEL_ACTUAL_TEXT_TOP);
        VDP_clearTileMapRect(BG_B, NOVEL_BG_LEFT, NOVEL_ACTUAL_TEXT_TOP, NOVEL_BG_WIDTH, NOVEL_BG_TOP + NOVEL_BG_HEIGHT - NOVEL_ACTUAL_TEXT_TOP);

        SYS_doVBlankProcess();
    }

    for(int i = 0; i < number_of_choices; i++) {
        int len = strlen(bin) + 1;
        if (i < double_row_start ) {
            VDP_drawText(bin, NOVEL_TEXT_LEFT + 1, NOVEL_ACTUAL_TEXT_TOP + i);
        } else {
            VDP_drawText(bin, NOVEL_TEXT_LEFT + 18, NOVEL_ACTUAL_TEXT_TOP + i - double_row_start);
        }
        
        bin += len;
        count += len;
    }
    JOY_setEventHandler(novel_choice_event_handler);
    while (!NOVEL.selected)
    {
        if (NOVEL_VARIABLES[0] < 0) {
            NOVEL_VARIABLES[0] = number_of_choices - 1;
        } else if (NOVEL_VARIABLES[0] >= number_of_choices) {
            NOVEL_VARIABLES[0] = 0;
        }
        for (int i = 0; i < number_of_choices; i++) {
            if (i < double_row_start) {
                VDP_clearText(NOVEL_TEXT_LEFT, NOVEL_ACTUAL_TEXT_TOP + i, 1);
            } else {
                VDP_clearText(NOVEL_TEXT_LEFT + 17, NOVEL_ACTUAL_TEXT_TOP + i - double_row_start, 1);
            }
            
        }
        if (NOVEL_VARIABLES[0] < double_row_start) {
            VDP_drawText(NOVEL_CHOICE_CHAR, NOVEL_TEXT_LEFT, NOVEL_ACTUAL_TEXT_TOP + NOVEL_VARIABLES[0]);
        } else {
            VDP_drawText(NOVEL_CHOICE_CHAR, NOVEL_TEXT_LEFT + 17, NOVEL_ACTUAL_TEXT_TOP + NOVEL_VARIABLES[0] - double_row_start);
        }
        
        SYS_doVBlankProcess();
        if (NOVEL.pause_menu) {
            JOY_setEventHandler(novel_event_handler);
            clear_text();
            NOVEL.selected = FALSE;
            if (new_lines) {
                VDP_setTileMapEx(BG_B, NOVEL_BACKGROUND[NOVEL.back_index]->tilemap, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, TILE_USERINDEX), NOVEL_BG_LEFT, NOVEL_ACTUAL_TEXT_TOP,  0,  NOVEL_BG_HEIGHT - new_lines, NOVEL_BG_WIDTH, new_lines, DMA_QUEUE);
                NOVEL_ACTUAL_TEXT_TOP = NOVEL_TEXT_TOP;  
                VDP_setWindowVPos(TRUE, NOVEL_TEXT_TOP);
            }
            return 0;
        }
    }
    JOY_setEventHandler(novel_event_handler);
    clear_text();
    NOVEL_VARIABLES[0] +=1;
    NOVEL.selected = FALSE;
    if (new_lines) {
        VDP_setTileMapEx(BG_B, NOVEL_BACKGROUND[NOVEL.back_index]->tilemap, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, TILE_USERINDEX), NOVEL_BG_LEFT, NOVEL_ACTUAL_TEXT_TOP,  0,  NOVEL_BG_HEIGHT - new_lines, NOVEL_BG_WIDTH, new_lines, DMA_QUEUE);
        NOVEL_ACTUAL_TEXT_TOP = NOVEL_TEXT_TOP;  
        VDP_setWindowVPos(TRUE, NOVEL_TEXT_TOP);
    }
    
    return count;
}




void novel_update() {
    int novel_function;
    NOVEL.advance = FALSE;
    NOVEL.selected = FALSE;
    u16 joy = JOY_readJoypad(JOY_1);
    if (joy & BUTTON_C) {
        NOVEL.advance = TRUE;
    }
    if (NOVEL.position >= NOVEL_SCRIPTS_BYTES_COUNT[NOVEL.script_index]) {
        novel_save_n_restart();
    }
    novel_function = *get_pos();
    switch (novel_function)
    {
    case 0: //bgload image.png fadetime
        NOVEL.position++;
        int back_index = read_int();
        int fade_time = read_int();
        draw_background(back_index, fade_time);
        break;
    case 1: //setimg image.png x y
        NOVEL.position++;
        int fore_index = read_int();
        int x = read_int();
        int y = read_int();
        draw_foreground(fore_index, x , y);
        break;
    case 2: //SOUND
        {
            NOVEL.position++;
            int sound_pos = read_int();
            int loop = read_char();
            if (loop == 255) {
                loop = 1;
            } else {
                loop = 0;
            }
            if(sound_pos == 32700) {
                novel_stop_sound();
            } else {
                NOVEL_PLAY_SOUND[sound_pos](loop);
            }
        }
        break;
    case 3: //MUSIC
        {
            NOVEL.position++;
            
            int music_pos = read_int();
            
            if (music_pos == NOVEL_NO_MUSIC) {
                novel_stop_music();
            } else {
                NOVEL_PLAY_MUSIC[music_pos]();
            }
            NOVEL.music = music_pos;
            
        }
        break;
    case 4: //TEXT
        {
            NOVEL.position += draw_text(get_pos()+1);
            break;
        }
    case 5: //CHOICE
        NOVEL.position += make_choice(get_pos()+1);
        //draw_int(NOVEL_VARIABLES[0], 2, 25);
        break;
    case 6: //SETVAR
        {
            NOVEL.position++;
            int var_index = read_int();
            int symbol = read_char();
            int num = read_int();

            int type = read_char();
            if (type == 1) { //IT is a Variable
                num = NOVEL_VARIABLES[num];
            } else if (type == 2) { //It is retfile to retfile
                num = NOVEL_VARIABLES[num];
            } else if (type == 3) { //It is scriptfile to retfile
 
            } else if (type == 4) { //It is retlabel to retlabel
                num = NOVEL_VARIABLES[num];
            } else if (type == 5) { //It is label name to retlabel

            }
            switch (symbol)
            {
            case 0:
                NOVEL_VARIABLES[var_index] = num;
                break;
            case 1:
                NOVEL_VARIABLES[var_index] += num;
                break;
            case 2:
                NOVEL_VARIABLES[var_index] -= num;
                break;
            default:
                break;
            }


        }
        //novel_update();
        break;
    case 7: //GSETVAR
        break;
    case 8: //IF
        NOVEL.position++;
        int variable = read_int();
        int eq = read_char();
        int num = read_int();
        int type = read_char();
        if (type == 1) { //VARIABLE
            num = NOVEL_VARIABLES[num];
        }

        int pass = FALSE;
        if (eq == 0) {  // ==
            if (NOVEL_VARIABLES[variable] == num) {
                pass = TRUE;
            }
        }  else if (eq == 1) { // !=
            if (NOVEL_VARIABLES[variable] != num) {
                pass = TRUE;
            }
        }  else if (eq == 2) { // >
            if (NOVEL_VARIABLES[variable] > num) {
                pass = TRUE;
            }
        }  else if (eq == 3) { // <
            if (NOVEL_VARIABLES[variable] < num) {
                pass = TRUE;
            }
        }  else if (eq == 4) { // >=
            if (NOVEL_VARIABLES[variable] >= num) {
                pass = TRUE;
            }
        }  else if (eq == 5) { // <=
            if (NOVEL_VARIABLES[variable] <= num) {
                pass = TRUE;
            }
        }
        if (pass) {
            NOVEL.position +=2;
        } else {
            NOVEL.position += read_int() - 2;
        }
        //novel_update();
        break;
    case 9: //FI
        NOVEL.position++;
        //novel_update();
        break;
    case 10: //JUMP
        {
            NOVEL.position++;
            int new_script_index = read_int();
            NOVEL.position = read_s32();
            NOVEL.script_index = new_script_index;
        }
        break;
    case 11: //DELAY
        {
            NOVEL.position++;
            int delay = read_int();
            for (int i = 0; i < delay; i++) {
                if (NOVEL.advance) {
                    i +=10;
                }
                SYS_doVBlankProcess();
            }
        }
        
        
        break;
    case 12: //RANDOM
        break;
    case 13: //LABEL
        break;
    case 14: //GO_TO
        NOVEL.position++;
        NOVEL.position = read_s32();

        
        break;
    case 15: //CLEAR_TEXT
        clear_text();

        break;
    case 16: //RESET VARS Custom command made for setvar ~ ~
        NOVEL.position++;
        novel_reset_vars();

        break;
    case 17: //RETJUMP this is when a line is like this: jump $RETFILE $RETLABEL
        NOVEL.position++;
        NOVEL.script_index = NOVEL_VARIABLES[NOVEL_RETFILE_INDEX];
        NOVEL.position = NOVEL_VARIABLES[NOVEL_RETLABEL_INDEX];
        break;
    default:

        break;
    }
    
    novel_pause_menu();
    
    SYS_doVBlankProcess();
}