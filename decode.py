import numpy as np
import math
import turtle
from huffman_decoder import *
t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("white")

def draw_pixel(turtle, x, y, color):  # color is a tuple here
    turtle.setposition(x, y)
    turtle.dot(1, color)
    return

def matrix_operations(ZZ, MCU, quant):
    temp = [0] * 64
    for i in range(64):
        temp[ZZ[i]] = MCU[i]
    for i in range(64):
        temp[i] *= quant[i]
    MCU = [list(range(8)) for i in range(8)]
    for i in range(8):
        for j in range(8):
            MCU[i][j] = temp[i + j]
    return MCU

def NormCoeff(n):
    if n == 0:
        return 1.0 / math.sqrt(2.0)
    else:
        return 1.0

idct_table = [
        [
            (NormCoeff(u) * math.cos(((2.0 * x + 1.0) * u * math.pi) / 16.0))
            for x in range(8)
        ]
        for u in range(8)
    ]

def IDCT(MCU, idct_table):
        out = [list(range(8)) for i in range(8)]

        for x in range(8):
            for y in range(8):
                local_sum = 0
                for u in range(8):
                    for v in range(8):
                        local_sum += (
                            MCU[v][u]
                            * idct_table[u][x]
                            * idct_table[v][y]
                        )
                out[y][x] = local_sum // 4
                return out
    
        
        



zigzag = [0, 1, 5, 6, 14, 15, 27, 28, 2, 4, 7, 13, 16, 26, 29, 42, 3, 8, 12, 17, 25, 30, 41, 43, 9, 11, 18, 24, 31, 40, 44, 53, 10, 19, 23, 32, 39, 45, 52, 54, 20, 22, 33, 38, 46, 51, 55, 60, 21, 34, 37, 47, 50, 56, 59, 61, 35, 36, 48, 49, 57, 58, 62, 63]

# Quantization tables

DQT0 = [ 16, 11, 10, 16, 24, 40, 51, 61,
         12, 12, 14, 19, 26, 58, 60, 55, 
         14, 13, 16, 24, 40, 57, 69, 56, 
         14, 17, 22, 29, 51, 87, 80, 62, 
         18, 22, 37, 56, 68, 109, 103, 77, 
         24, 35, 55, 64, 81, 104, 113, 92, 
         49, 64, 78, 87, 103, 121, 120, 101,
         72, 92, 95, 98, 112, 100, 103, 99 ]

DQT1 = [ 17, 18, 24, 47, 99, 99, 99, 99,
         18, 21, 26, 66, 99, 99, 99, 99, 
         24, 26, 56, 99, 99, 99, 99, 99, 
         47, 66, 99, 99, 99, 99, 99, 99, 
         99, 99, 99, 99, 99, 99, 99, 99, 
         99, 99, 99, 99, 99, 99, 99, 99, 
         99, 99, 99, 99, 99, 99, 99, 99, 
         99, 99, 99, 99, 99, 99, 99, 99 ]

# Huffman tables
bitstream = [[0], [-1, 1], list(range(-3, -1)) + list(range(2, 4)), list(range(-7, -3)) + list(range(4, 8)), list(range(-15, -7)) + list(range(8, 16)), list(range(-31, -15)) + list(range(16, 32)), list(range(-63, -31)) + list(range(32, 64))]

def BitStream(category, bits, stream):
    stream[category]

    if bits < 2**(category - 1):
        val = 1 - 2**(category) + bits
    else:
        val = bits
    return val


DHT10 = "10 00 02 01 03 03 02 04 03 05 05 04 04 00 00 01 7D 01 02 03 00 04 11 05 12 21 31 41 06 13 51 61 07 22 71 14 32 81 91 A1 08 23 42 B1 C1 15 52 D1 F0 24 33 62 72 82 09 0A 16 17 18 19 1A 25 26 27 28 29 2A 34 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 83 84 85 86 87 88 89 8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E1 E2 E3 E4 E5 E6 E7 E8 E9 EA F1 F2 F3 F4 F5 F6 F7 F8 F9 FA"
DHT10 = DHT10.split(" ")
for i in range(len(DHT10)): DHT10[i] = int(DHT10[i], 16)
DHT01 = "01 00 03 01 01 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 04 05 06 07 08 09 0A 0B"
DHT01 = DHT01.split(" ")
for i in range(len(DHT01)): DHT01[i] = int(DHT01[i], 16)
DHT11 = "11 00 02 01 02 04 04 03 04 07 05 04 04 00 01 02 77 00 01 02 03 11 04 05 21 31 06 12 41 51 07 61 71 13 22 32 81 08 14 42 91 A1 B1 C1 09 23 33 52 F0 15 62 72 D1 0A 16 24 34 E1 25 F1 17 18 19 1A 26 27 28 29 2A 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 82 83 84 85 86 87 88 89 8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E2 E3 E4 E5 E6 E7 E8 E9 EA F2 F3 F4 F5 F6 F7 F8 F9 FA"
DHT11 = DHT11.split(" ")
for i in range(len(DHT11)): DHT11[i] = int(DHT11[i], 16)

H10 = H_tree()
H10.gen(DHT10[1:17],DHT10[17:])
H11 = H_tree()
H11.gen(DHT11[1:17],DHT11[17:])
H01 = H_tree()
H01.gen(DHT01[1:17],DHT01[17:])


f = open('dat.txt', 'r')
dat = f.read()
dat = re.split(' |\n', dat)

MCU = []
dc = 0

while len(dat):
    decoded, dat = H01.decode(dat)
    size = decoded
    dc_temp = 0

    while size:
        if not H01.dec_pos:
            H01.last_byte = int(dat.pop(0), 16)
    
        shift = 8 - size - H01.dec_pos
        
        for i in range(H01.dec_pos, 8):
            if not size:
                break
            dc_temp += (H01.last_byte & (0b10000000 >> i))/2**(shift)
            H01.dec_pos += 1
            H01.dec_pos = H01.dec_pos % 8
            size -= 1


    dc += BitStream(decoded, dc_temp, bitstream)
    MCU.append(dc)

    H11.last_byte = H01.last_byte
    H11.dec_pos = H01.dec_pos

    while 1:
        decoded, dat = H11.decode(dat)
        zeros = (decoded & 0xf0) >> 4
        MCU += zeros * [0]
        size = decoded & 0x0f
        val = 0
        while size:
            if not H11.dec_pos:
                H11.last_byte = int(dat.pop(0), 16)
        
            shift = 8 - size - H11.dec_pos
        
            for i in range(H11.dec_pos, 8):
                if not size:
                    break
                val += (H11.last_byte & (0b10000000 >> i))/2**(shift)
                H11.dec_pos += 1
                H11.dec_pos = H11.dec_pos % 8
                size -= 1

        MCU.append(BitStream(decoded & 0x0f, val, bitstream))
        if not BitStream(decoded & 0x0f, val, bitstream):
            H01.last_byte = H11.last_byte
            H01.dec_pos = H11.dec_pos + decoded
            break

    MCU += [0] * (64 - len(MCU))
    out = IDCT(matrix_operations(zigzag, MCU, DQT0), idct_table)
    
    print(out)
    for i in range(8):
        for j in range(8):
            #draw_pixel(t, i, j, (out[i][j]))
            quit

    

