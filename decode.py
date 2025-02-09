import re
import numpy as np
from scipy.fftpack import idct
import turtle
from huffman_decoder import *
t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("white")
screen.tracer(0)  # Disable animation
t.penup()

def draw_pixel(turtle, x, y, color):  # color is a tuple here
    turtle.setposition(x, y)
    turtle.dot(1, color)
    return

def clamp(num):
    if num < 0: return 0
    elif num > 256: return 256
    else: return num

def IDCT(array_8x8):
    # Perform IDCT along rows (axis=1)
    idct_rows = idct(array_8x8, axis=1, norm='ortho')

    # Perform IDCT along columns (axis=0)
    idct_2d = idct(idct_rows, axis=0, norm='ortho')

    return idct_2d
    
def matrix_operations(ZZ, MCU, quant):
    ret = [[0, 0, 0, 0, 0, 0, 0, 0],  # bruh
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(8):
        for j in range(8):
            ret[i][j] = MCU[ZZ[i][j]] * quant[i][j]
    return ret


zigzag = [[0 , 1 , 5 , 6 , 14, 15, 27, 28],
          [2 , 4 , 7 , 13, 16, 26, 29, 42],
          [3 , 8 , 12, 17, 25, 30, 41, 43],
          [9 , 11, 18, 24, 31, 40, 44, 53],
          [10, 19, 23, 32, 39, 45, 52, 54],
          [20, 22, 33, 38, 46, 51, 55, 60],
          [21, 34, 37, 47, 50, 56, 59, 61],
          [35, 36, 48, 49, 57, 58, 62, 63]]

# Quantization tables

DQT0 = [ [10, 7 , 6 , 10, 15, 25, 32, 38],
         [8 , 8 , 9 , 12, 16, 36, 38, 34], 
         [9 , 8 , 10, 15, 25, 36, 43, 35], 
         [9 , 11, 14, 18, 32, 54, 50, 39], 
         [11, 14, 23, 35, 43, 68, 64, 48], 
         [15, 22, 34, 40, 51, 65, 71, 58], 
         [31, 40, 49, 54, 64, 76, 75, 63],
         [45, 58, 59, 61, 70, 63, 64, 62] ]

DQT1 = [ [11, 11, 15, 29, 62, 62, 62, 62],
         [11, 13, 16, 41, 62, 62, 62, 62], 
         [15, 16, 35, 62, 62, 62, 62, 62], 
         [29, 41, 62, 62, 62, 62, 62, 62], 
         [62, 62, 62, 62, 62, 62, 62, 62], 
         [62, 62, 62, 62, 62, 62, 62, 62], 
         [62, 62, 62, 62, 62, 62, 62, 62], 
         [62, 62, 62, 62, 62, 62, 62, 62] ]

def BitStream(category, bits):

    if bits < 2**(category - 1):
        val = 1 - 2**(category) + bits
    else:
        val = bits
    return val

# somdeday I'll clean this bit up

DHT00 = "00 00 01 05 01 01 01 01 01 01 00 00 00 00 00 00 00 00 01 02 03 04 05 06 07 08 09 0A 0B"
DHT00 = DHT00.split(" ")
for i in range(len(DHT00)): DHT00[i] = int(DHT00[i], 16)
DHT10 = "10 00 02 01 03 03 02 04 03 05 05 04 04 00 00 01 7D 01 02 03 00 04 11 05 12 21 31 41 06 13 51 61 07 22 71 14 32 81 91 A1 08 23 42 B1 C1 15 52 D1 F0 24 33 62 72 82 09 0A 16 17 18 19 1A 25 26 27 28 29 2A 34 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 83 84 85 86 87 88 89 8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E1 E2 E3 E4 E5 E6 E7 E8 E9 EA F1 F2 F3 F4 F5 F6 F7 F8 F9 FA"
DHT10 = DHT10.split(" ")
for i in range(len(DHT10)): DHT10[i] = int(DHT10[i], 16)
DHT01 = "01 00 03 01 01 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 04 05 06 07 08 09 0A 0B"
DHT01 = DHT01.split(" ")
for i in range(len(DHT01)): DHT01[i] = int(DHT01[i], 16)
DHT11 = "11 00 02 01 02 04 04 03 04 07 05 04 04 00 01 02 77 00 01 02 03 11 04 05 21 31 06 12 41 51 07 61 71 13 22 32 81 08 14 42 91 A1 B1 C1 09 23 33 52 F0 15 62 72 D1 0A 16 24 34 E1 25 F1 17 18 19 1A 26 27 28 29 2A 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 82 83 84 85 86 87 88 89 8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E2 E3 E4 E5 E6 E7 E8 E9 EA F2 F3 F4 F5 F6 F7 F8 F9 FA"
DHT11 = DHT11.split(" ")
for i in range(len(DHT11)): DHT11[i] = int(DHT11[i], 16)

H11 = H_tree()
H11.gen(DHT11[1:17],DHT11[17:])
H00 = H_tree()
H00.gen(DHT00[1:17],DHT00[17:])
H01 = H_tree()
H01.gen(DHT01[1:17],DHT01[17:])
H10 = H_tree()
H10.gen(DHT10[1:17],DHT10[17:])



f = open('oliver_dat.txt', 'r')
dat = f.read()
dat = re.split(' |\n', dat)
dc_L = 0
dc_C = 0

for y in range(30):
    for x in range(20):
        MCU_coords = [[16*x, 8*y], [8 + 16*x, 8*y]]
        for m in range(2):  # this is derived from the sampling factor
            MCU = []
            decoded, dat = H00.decode(dat)
            size = decoded
            dc_temp = 0

            while size:
                if not H00.dec_pos:
                    H00.last_byte = int(dat.pop(0), 16)
    
                shift = 8 - size - H00.dec_pos
        
                for i in range(H00.dec_pos, 8):
                    if not size:
                        break
                    dc_temp += (H00.last_byte & (0b10000000 >> i))/2**(shift)
                    H00.dec_pos += 1
                    H00.dec_pos = H00.dec_pos % 8
                    size -= 1


            dc_L += BitStream(decoded, dc_temp)
            MCU.append(dc_L)

            H10.last_byte = H00.last_byte
            H10.dec_pos = H00.dec_pos

            while 1:
                decoded, dat = H10.decode(dat)
                zeros = (decoded & 0xf0) >> 4
                MCU += zeros * [0]
                size = decoded & 0x0f
                val = 0
                while size:
                    if not H10.dec_pos:
                        H10.last_byte = int(dat.pop(0), 16)
        
                    shift = 8 - size - H10.dec_pos
        
                    for i in range(H10.dec_pos, 8):
                        if not size:
                            break
                        val += (H10.last_byte & (0b10000000 >> i))/2**(shift)
                        H10.dec_pos += 1
                        H10.dec_pos = H10.dec_pos % 8
                        size -= 1

                MCU.append(BitStream(decoded & 0x0f, val))
                if not BitStream(decoded & 0x0f, val):
                    H00.last_byte = H10.last_byte
                    H00.dec_pos = H10.dec_pos
                    break

            MCU += [0] * (64 - len(MCU))
            out = IDCT(np.array(matrix_operations(zigzag, MCU, DQT0), dtype=float))
            for i in range(8):
                for j in range(8):
                    draw_pixel(t, MCU_coords[m][0] + j, -MCU_coords[m][1] + (7 - i), (clamp(out[i][j] + 128)/256, clamp(out[i][j] + 128)/256, clamp(out[i][j] + 128)/256))

        H01.last_byte = H00.last_byte
        H01.dec_pos = H00.dec_pos

        for m in range(2):
            MCU = []
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


            dc_C += BitStream(decoded, dc_temp)
            MCU.append(dc_C)

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

                MCU.append(BitStream(decoded & 0x0f, val))
                if not BitStream(decoded & 0x0f, val):
                    H01.last_byte = H11.last_byte
                    H01.dec_pos = H11.dec_pos
                    break
        H00.last_byte = H01.last_byte
        H00.dec_pos = H01.dec_pos

screen.update()
screen.mainloop()
