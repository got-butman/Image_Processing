
class Node: # Standard recursive node adapted to track layer for assisting decoding 
    def __init__(self, val, layer):
        self.val = val
        self.layer = layer
        self.left = None
        self.right = None

class H_tree: # Huffman tree
    def __init__(self):
        self.root = Node(-1, None)
        
        # To help keep track while decoding
        self.dec_pos = 0
        self.last_byte = 0

    def gen(self, count, sym):
        self.root.left = Node(None,  0)
        self.root.right = Node(None,  0)
        self._add(count, sym, self.root.left)
        self._add(count, sym, self.root.right)


    def _add(self, count, sym, node):
        if len(sym) == 0:
            return
        
        if count[node.layer] != 0:
            node.val = sym.pop(0)
            count[node.layer] -= 1
        elif len(sym) == 2:  # accounts for last row in H tree
            node.left = Node(sym.pop(0), node.layer + 1)
            node.right = Node(sym.pop(0), node.layer + 1)
            self._add(count, sym, node.left)
            self._add(count, sym, node.right)
        else:
            node.left = Node(None, node.layer + 1)
            node.right = Node(None, node.layer + 1)
            self._add(count, sym, node.left)
            self._add(count, sym, node.right)

    def view(self):  # left > root > right
        if self.root:
            self._view(self.root)
        
    def _view(self, node):
        if node:
            self._view(node.left)
            print(str(node.val) + '(' + str(node.layer) +')', end = " ")
            self._view(node.right)

    def decode(self, dat):
        decoded = 0
        node = self.root

        while len(dat):
            if not self.dec_pos:
                self.last_byte = int(dat.pop(0), 16)

            for i in range(self.dec_pos, 8):

                if self.last_byte & (0b10000000 >> i):
                    node = node.right
                else:
                    node = node.left
                
                self.dec_pos += 1
                self.dec_pos = self.dec_pos % 8
                
                if (node.left == None) and (node.right == None):
                    decoded = node.val
                    return decoded, dat

if __name__ == '__main__':

    # example using DC table 1

    DHT = "11 00 02 01 02 04 04 03 04 07 05 04 04 00 01 02 77 00 01 02 03 11 04 05 21 31 06 12 41 51 07 61 71 13 22 32 81 08 14 42 91 A1 B1 C1 09 23 33 52 F0 15 62 72 D1 0A 16 24 34 E1 25 F1 17 18 19 1A 26 27 28 29 2A 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 82 83 84 85 86 87 88 89 8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E2 E3 E4 E5 E6 E7 E8 E9 EA F2 F3 F4 F5 F6 F7 F8 F9 FA"
    HT = DHT.split(" ")

    for i in range(len(HT)): HT[i] = int(HT[i], 16)

    dat = HT[0] # AC/DC + table no.
    ent = HT[1:17] # "inverse entropy"
    sym = HT[17:] # symbols

    H = H_tree()
    H.gen(ent, sym)
    #H.view()

    print(H.decode(['0xFF', '0x96']))
