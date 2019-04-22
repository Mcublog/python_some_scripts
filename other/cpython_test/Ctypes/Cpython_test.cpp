#include "Cpython_test.h"
#include <stdio.h>

extern "C" __declspec(dllexport) int test_function(void)
{
    static int i = 0;
    return i++;
}

