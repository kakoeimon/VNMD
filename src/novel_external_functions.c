#include "genesis.h"
#include "novel_player.h"
#include "novel_functions.h"
#include "novel_scripts.h"
#include "novel_images.h"
#include "novel_sounds.h"
#include "novel_variables.h"
#include "novel_external_functions.h"

void reset() {
    novel_reset();
}


void fade_out() {
    PAL_fadeOutAll(60, FALSE);
    PAL_setColor(31, RGB24_TO_VDPCOLOR(0xffffff)); //Set the 31 color to white cause this is the color of the text
}


void ret_jump_store() {
    NVAR_retfile = NOVEL.script_index;
    NVAR_retlabel = NOVEL.position  + 7; //Seven cause that's how long a jump is in bytes.
}

void ret_return() {
    NOVEL.script_index = NVAR_retfile;
    NOVEL.position = NVAR_retlabel;
}

void fr_clear() {
    novel_draw_background(NOVEL.back_index, 0);
}