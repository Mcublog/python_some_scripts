#pragma once
#include <windows.h>
#include <stdio.h>
#include <stdint.h>

typedef struct
{
    uint32_t time;
    uint16_t t_ms;
    uint16_t day;
    uint16_t date;
}time_stamp_t;

extern "C" __declspec(dllexport) int test_function(void);
extern "C" __declspec(dllexport) int test_function_struct(time_stamp_t *t);
