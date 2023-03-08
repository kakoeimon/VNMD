#ifndef H_NV_EXTERNAL_FUNCTIONS
#define H_NV_EXTERNAL_FUNCTIONS

#define NV_EXTERNAL_FUNCTIONS_NUM 4

extern void (*nv_external_functions[])();

void reset();
void fade_out();
void ret_jump_store();
void ret_return();

#endif
