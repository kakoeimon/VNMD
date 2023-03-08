#include <genesis.h>

#include "novel_player.h"

#ifdef GR_LANG
#include "grres.h"
#endif

int main(bool hard)
{
    #ifdef GR_LANG
    VDP_loadFont(&greek_font, DMA);
    #endif
    
    XGM_setMusicTempo(60);
    novel_reset();
    while(TRUE) {

        novel_update();
        
    }
    return 0;
}

