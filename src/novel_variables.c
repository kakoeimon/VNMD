#include "novel_variables.h"
#include "novel_external_functions.h"

const int NOVEL_SAVE_CHECK_NUM = 1234;

const int NOVEL_NUM_VARIABLES = 3;
const int NOVEL_NUM_GLOBAL_VARIABLES = 0;

int NOVEL_VARIABLES[3];
void (*nv_external_functions[])() = {
	reset,
	fade_out,
	ret_jump_store,
	ret_return,
};