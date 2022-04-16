#include "genesis.h"
#include "novel_player.h"
#include "novel_functions.h"
#include "novel_scripts.h"
#include "novel_images.h"
#include "novel_variables.h"

char NOVEL_CHOICE_CHAR[1] = {'z' + 5};


int NOVEL_PAUSE_MENU_POS = 0;
int NOVEL_PAUSE_MENU_SELECTED = FALSE;


int bytes_to_int(int byte1, int byte2) {
    return byte2 | byte1 << 8;
}


u8 *get_pos() {
    return FAR_SAFE(NOVEL_SCRIPTS[NOVEL_SCR_INDEX]+NOVEL_POSITION, NOVEL_SCRIPTS_BYTES_COUNT[NOVEL_SCR_INDEX]);
}

u8 read_char() {
    u8 r = *get_pos();
    NOVEL_POSITION++;
    return r;
}

int read_int() {
    u8 a = *get_pos();
    NOVEL_POSITION++;
    u8 b = *get_pos();
    NOVEL_POSITION++;
    return b | a << 8;
}


u16 read_u16() {
    u8 a = *get_pos();
    NOVEL_POSITION++;
    u8 b = *get_pos();
    NOVEL_POSITION++;
    return b | a << 8;
}


s32 read_s32() {
    u8 a = *get_pos();
    NOVEL_POSITION++;
    u8 b = *get_pos();
    NOVEL_POSITION++;
    u8 c = *get_pos();
    NOVEL_POSITION++;
    u8 d = *get_pos();
    NOVEL_POSITION++;
    //long result = (((bytes[0] << 8 & bytes[1]) << 8 & bytes[2]) << 8) & bytes[3]
    return d | c << 8 | b << 16 | a << 24;;
}

void clear_text() {
    VDP_clearPlane(WINDOW, FALSE);
}


void novel_event_handler(u16 joy, u16 changed, u16 state) {
    if (joy == JOY_1) {
        if (state & changed & BUTTON_A || state & changed & BUTTON_C) {
            NOVEL_ADVANCE = TRUE;
        } else if (state & changed & BUTTON_START) {
            NOVEL_PAUSE_MENU = TRUE;
            

        }
    }
}

void novel_choice_event_handler(u16 joy, u16 changed, u16 state) {
    if (state & changed & BUTTON_UP) {
        NOVEL_VARIABLES[0] -= 1;
    } else if (state & changed & BUTTON_DOWN) {
        NOVEL_VARIABLES[0] += 1;
    }  else if (state & changed & BUTTON_B) {
        NOVEL_SELECTED = TRUE;
    } else if (state & changed & BUTTON_START) {
        NOVEL_PAUSE_MENU = TRUE;
    }
}

void novel_change_pal_for_text() {
    PAL_setColor(15, RGB24_TO_VDPCOLOR(0xffffff));
    PAL_setColor(0, RGB24_TO_VDPCOLOR(0x000000));
}

void novel_set_bg_palette() {
    PAL_setPalette(PAL0, NOVEL_BACKGROUND[NOVEL_BACK_INDEX]->palette->data, CPU);
}


void novel_pause_event_handler(u16 joy, u16 changed, u16 state) {
    if (state & changed & BUTTON_UP) {
        NOVEL_PAUSE_MENU_POS -= 1;
    } else if (state & changed & BUTTON_DOWN) {
        NOVEL_PAUSE_MENU_POS += 1;
    }  else if (state & changed & BUTTON_B) {
        NOVEL_PAUSE_MENU_SELECTED = TRUE;
    } else if (state & changed & BUTTON_START) {
        NOVEL_PAUSE_MENU = FALSE;
    }
}

void novel_pause_menu_set_cursor(int max_values) {
    for (int i = 0; i < 3; i++) {
        VDP_clearText(NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + i, 1);
    }
        if (NOVEL_PAUSE_MENU_POS < 0) NOVEL_PAUSE_MENU_POS = max_values - 1;
        if (NOVEL_PAUSE_MENU_POS >= max_values) NOVEL_PAUSE_MENU_POS = 0;
        VDP_drawText(NOVEL_CHOICE_CHAR, NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + NOVEL_PAUSE_MENU_POS);
}

int novel_get_save_index() {
    int base_length = 4 + NOVEL_NUM_GLOBAL_VARIABLES * 2;
    int save_length = NOVEL_NUM_VARIABLES * 2 + 2 + 2 + 6 * 3 + 4 + 2;
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
    SRAM_writeLong(index, NOVEL_POSITION);
    index +=4;
    SRAM_writeWord(index, NOVEL_SCR_INDEX);
    index += 2;
    SRAM_writeWord(index, NOVEL_BACK_INDEX);
    index +=2;
    for (int i = 0; i < 3; i++) {
        SRAM_writeWord(index, NOVEL_FORE_IMGS[i]);
        index +=2;
        SRAM_writeWord(index, NOVEL_FORE_IMGS_POS[i][0]);
        index +=2;
        SRAM_writeWord(index, NOVEL_FORE_IMGS_POS[i][1]);
        index +=2;
    }
    
    for (int i = 0; i < NOVEL_NUM_VARIABLES; i++) {
        SRAM_writeWord(index + i*2, NOVEL_VARIABLES[i]);
    }

    SRAM_disable();
    
    for (int i = 0; i < 60; i++) {
        SYS_doVBlankProcess();
    }
    
}

void novel_load() {
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
        NOVEL_POSITION = SRAM_readLong(index);
        index +=4;
        NOVEL_SCR_INDEX = SRAM_readWord(index);
        index += 2;
        int tmp_bg = SRAM_readWord(index);
        index +=2;
        for (int i = 0; i < 3; i++) {
            tmp_img[i] = SRAM_readWord(index);
            index +=2;
            NOVEL_FORE_IMGS_POS[i][0] = SRAM_readWord(index);
            index +=2;
             NOVEL_FORE_IMGS_POS[i][1] = SRAM_readWord(index);
            index +=2;
        }
    
        for (int i = 0; i < NOVEL_NUM_VARIABLES; i++) {
            NOVEL_VARIABLES[i] = SRAM_readWord(index + i*2);
        }
        SRAM_disable();

        draw_background(tmp_bg, 16);
        for (int i = 0; i < 3; i++) {
            if (tmp_img[i] != MAX_S16) {
                draw_foreground(tmp_img[i], NOVEL_FORE_IMGS_POS[i][0], NOVEL_FORE_IMGS_POS[i][1]);
            }
        }
        NOVEL_PAUSE_MENU = FALSE;
        
    } else {
        SRAM_disable();
        VDP_drawText("Empty Slot", NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP);
        for (int i = 0; i < 60; i++) {
            SYS_doVBlankProcess();
        }
    }


    
    
    
}

void novel_vblank_callback() {
    novel_set_bg_palette();
    if (NOVEL_PAUSE_MENU) {
        NOVEL_INTERAPTED = TRUE;
        SYS_setVBlankCallback(novel_set_bg_palette);
        JOY_setEventHandler(novel_pause_event_handler);
        NOVEL_PAUSE_MENU_POS = 0;
        NOVEL_PAUSE_MENU_SELECTED = FALSE;
        
        clear_text();
        SYS_doVBlankProcess();

        VDP_drawText("Save", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
        VDP_drawText("Load", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
        VDP_drawText("Return to title Screen", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);

        NOVEL_PAUSE_MENU_SELECTED = FALSE;
        while (!NOVEL_PAUSE_MENU_SELECTED && NOVEL_PAUSE_MENU)
        {   
            
            novel_pause_menu_set_cursor(3);
            SYS_doVBlankProcess();
        }
        if (NOVEL_PAUSE_MENU_SELECTED) { 
            NOVEL_PAUSE_MENU_SELECTED = FALSE;
            if (NOVEL_PAUSE_MENU_POS == 0) {
                clear_text();
                VDP_drawText("Save Slot 1", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
                VDP_drawText("Save Slot 2", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
                VDP_drawText("Save Slot 3", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);
                NOVEL_PAUSE_MENU_SELECTED = FALSE;
                while (!NOVEL_PAUSE_MENU_SELECTED && NOVEL_PAUSE_MENU) {
                    novel_pause_menu_set_cursor(3);
                    SYS_doVBlankProcess();
                }
                if (NOVEL_PAUSE_MENU_SELECTED) {
                    novel_save();
                }

            } else if (NOVEL_PAUSE_MENU_POS == 1) {
                NOVEL_PAUSE_MENU_POS = 0;
                clear_text();

                VDP_drawText("Load Slot 1", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP);
                VDP_drawText("Load Slot 2", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+1);
                VDP_drawText("Load Slot 3", NOVEL_TEXT_LEFT+1, NOVEL_TEXT_TOP+2);
                NOVEL_PAUSE_MENU_SELECTED = FALSE;
                while (!NOVEL_PAUSE_MENU_SELECTED && NOVEL_PAUSE_MENU) {
                    novel_pause_menu_set_cursor(3);
                    SYS_doVBlankProcess();
                }
                if (NOVEL_PAUSE_MENU_SELECTED) {
                    novel_load();
                }
            } else if (NOVEL_PAUSE_MENU_POS == 2) {
                NOVEL_PAUSE_MENU = FALSE;
                novel_reset();
            }
        }
        
        clear_text();
        SYS_setVBlankCallback(novel_vblank_callback);
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
    NOVEL_POSITION = 0;
    NOVEL_SCR_INDEX = 0;
    NOVEL_BACK_INDEX = -1;

    for (int i = 0; i < 3; i++) {
        NOVEL_FORE_IMGS[i] = MAX_S16;
    }
    
    NOVEL_SELECTED = 0;
    //NOVEL_SCR_INDEX = 0;
    NOVEL_ADVANCE = FALSE;
    NOVEL_PAUSE_MENU = FALSE;


    JOY_setEventHandler(novel_event_handler);

    VDP_setWindowVPos(TRUE, NOVEL_TEXT_TOP);
    VDP_setTextPlane(WINDOW);

    VDP_setHInterrupt(TRUE);
    VDP_setHIntCounter(NOVEL_TEXT_TOP * 8 - 1);
    SYS_setHIntCallback(novel_change_pal_for_text);
    

    SYS_setVBlankCallback(novel_vblank_callback);

    novel_reset_vars();
}


int make_choice(const char *bin) {
    int count = 2;
    NOVEL_VARIABLES[0] = 0;
    NOVEL_INTERAPTED = FALSE;
    int number_of_choices = bin[0];
    bin++;
    for(int i = 0; i < number_of_choices; i++) {
        int len = strlen(bin) + 1;
        VDP_drawText(bin, NOVEL_TEXT_LEFT + 1, NOVEL_TEXT_TOP + i);
        bin += len;
        count += len;
    }
    JOY_setEventHandler(novel_choice_event_handler);
    while (!NOVEL_SELECTED)
    {
        if (NOVEL_VARIABLES[0] < 0) {
            NOVEL_VARIABLES[0] = number_of_choices - 1;
        } else if (NOVEL_VARIABLES[0] >= number_of_choices) {
            NOVEL_VARIABLES[0] = 0;
        }
        for (int i = 0; i < number_of_choices; i++) {
            VDP_clearText(NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + i, 1);
        }
        VDP_drawText(NOVEL_CHOICE_CHAR, NOVEL_TEXT_LEFT, NOVEL_TEXT_TOP + NOVEL_VARIABLES[0]);
        SYS_doVBlankProcess();
        if (NOVEL_INTERAPTED) {
            JOY_setEventHandler(novel_event_handler);
            clear_text();
            NOVEL_SELECTED = FALSE;
            return 0;
        }
    }
    JOY_setEventHandler(novel_event_handler);
    clear_text();
    NOVEL_VARIABLES[0] +=1;
    NOVEL_SELECTED = FALSE;
    return count;
}




void novel_update() {
    int novel_function;
    NOVEL_ADVANCE = FALSE;
    NOVEL_SELECTED = FALSE;
    u16 joy = JOY_readJoypad(JOY_1);
    if (joy & BUTTON_C) {
        NOVEL_ADVANCE = TRUE;
    }
    if (NOVEL_POSITION >= NOVEL_SCRIPTS_BYTES_COUNT[NOVEL_SCR_INDEX]) {
        novel_save_n_restart();
    }
    novel_function = *get_pos();
    switch (novel_function)
    {
    case 0: //bgload image.png fadetime
        NOVEL_POSITION++;
        int back_index = read_int();
        int fade_time = read_int();
        draw_background(back_index, fade_time);
        break;
    case 1: //setimg image.png x y
        NOVEL_POSITION++;
        int fore_index = read_int();
        int x = read_int();
        int y = read_int();
        draw_foreground(fore_index, x , y);
        break;
    case 2: //SOUND
        break;
    case 3: //MUSIC
        break;
    case 4: //TEXT
        {
            NOVEL_POSITION += draw_text(get_pos()+1);
            break;
        }
    case 5: //CHOICE
        NOVEL_POSITION += make_choice(get_pos()+1);
        //draw_int(NOVEL_VARIABLES[0], 2, 25);
        break;
    case 6: //SETVAR
        {
            NOVEL_POSITION++;
            int var_index = read_int();
            int symbol = read_char();
            int num = read_int();

            if (read_char() == 1) {
                num = NOVEL_VARIABLES[num];
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
        NOVEL_POSITION++;
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
        }  else if (eq == 4) { // <=
            if (NOVEL_VARIABLES[variable] <= num) {
                pass = TRUE;
            }
        }
        if (pass) {
            NOVEL_POSITION +=2;
        } else {
            NOVEL_POSITION += read_int() - 2;
        }
        //novel_update();
        break;
    case 9: //FI
        NOVEL_POSITION++;
        //novel_update();
        break;
    case 10: //JUMP
        {
            NOVEL_POSITION++;
            int new_script_index = read_int();
            NOVEL_POSITION = read_s32();
            NOVEL_SCR_INDEX = new_script_index;
        }
        break;
    case 11: //DELAY
        break;
    case 12: //RANDOM
        break;
    case 13: //LABEL
        break;
    case 14: //GO_TO
        NOVEL_POSITION++;
        NOVEL_POSITION = read_s32();

        
        break;
    case 15: //CLEAR_TEXT
        clear_text();

        break;
    case 16: //RESET VARS Custom command made for setvar ~ ~
        NOVEL_POSITION++;
        novel_reset_vars();

        break;
    default:

        break;
    }
    
    
    SYS_doVBlankProcess();
}