#include "Cpython_test.h"
#include <stdio.h>

extern "C" __declspec(dllexport) int test_function(void)
{
    static int i = 0;
    return i++;
}

extern "C" __declspec(dllexport) int test_function_struct(time_stamp_t *t)
{
    t->time = 1234;
    t->t_ms = 4321;
    t->day = 1;
    t->date = 105;

    return 0;
}
