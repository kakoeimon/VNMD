#ifndef H_NOVEL_PLAYER
#define H_NOVEL_PLAYER
//#define GR_LANG
void novel_reset();

void novel_update();

typedef struct ifchoice_{
    int display;
    int pos;
    char *text;
}ifchoice;

#endif