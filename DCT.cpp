#include "DCT.h"

void DCT2(float (&in)[8][8], float (&out)[8][8]) {
    for (int i = 0; i < 8; i++){
        for (int j = 0; j < 8; j++){
            for (int u = 0; u < 8; u++){
                out[i][j] += cos(i * 3.14159/4.0 * u);
            }
            for (int v = 0; v < 8; v++){
                out[i][j] += cos(j * 3.14159/4.0 * v);
            }
            out[i][j] *= 0.125;
        }
    }
}
