#include "E2E_P05.h"
#include <stdio.h>
#include <string.h>

E2E_P05ConfigType Config = {
        .Offset = 0x0000,
        .DataID = 0x1234,
        .DataLength = 64U,
        .MaxDeltaCounter = 1,
};

E2E_P05ProtectStateType State = {
        .Counter = 0,
};

int main(void) {
    uint8_t expected_buffer[16] = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x28, 0x91, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };

    uint8_t buffer[16];
    memset(buffer, 0, 16);
    Config.Offset = 64;
    Config.DataLength = 128;
    Std_ReturnType result = E2E_P05Protect(&Config, &State, buffer, 16);
    
    for (int i = 0; i<16; ++i) {
        if(buffer[i] != expected_buffer[i]){
            printf("i = %u, buffer[%d] = 0x%02X, expected_buffer[%d] = 0x%02X\n",
                   i, buffer[i], expected_buffer[i]);
        }
    }
    return 0;
}