#ifndef DCT_H
#define DCT_H

#include <cmath>

void DCT2(float (&in)[8][8], float (&out)[8][8]);  // Type 2
void DCT3(float (&in)[8][8], float (&out)[8][8]);  // IDCT (Tyoe 3)

#endif