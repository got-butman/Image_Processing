
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

    DHT = "01 00 03 01 01 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 04 05 06 07 08 09 0A 0B"
    HT = DHT.split(" ")

    for i in range(len(HT)): HT[i] = int(HT[i], 16)

    dat = HT[0] # AC/DC + table no.
    ent = HT[1:17] # "inverse entropy"
    sym = HT[17:] # symbols

    H = H_tree()
    H.gen(ent, sym)
    H.view()
