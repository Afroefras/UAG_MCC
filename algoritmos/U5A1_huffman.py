from collections import defaultdict


class Huffman:
    def __init__(self) -> None:
        pass

    def huffman_encoding(self, text: str) -> tuple:
        char_frec = defaultdict(int)
        for x in text:
            char_frec[x] += 1

        frecs = [(x, f) for x, f in char_frec.items()]
        frecs.sort(key=lambda x: x[1])

        huffman = {}
        while len(frecs) > 1:
            a, n = frecs.pop(0)
            b, m = frecs.pop(0)

            for x in a:
                huffman[x] = "0" + huffman.get(x, "")
            for x in b:
                huffman[x] = "1" + huffman.get(x, "")

            combined_freq = n + m

            i = 0
            while i < len(frecs) and combined_freq > frecs[i][1]:
                i += 1
            frecs.insert(i, ((a + b), combined_freq))

        encoded = "".join([huffman[x] for x in text])

        return encoded, huffman

    def huffman_decoding(self, encoded: bytes, huffman: dict) -> str:
        huff_rev = {v: k for k, v in huffman.items()}

        decoded = ""
        i = 0
        while i < len(encoded):
            j = i + 1
            while encoded[i:j] not in huff_rev:
                j += 1
            decoded += huff_rev[encoded[i:j]]
            i = j

        return decoded


FREQ = {"A": 5, "B": 12, "C": 35, "D": 3, "E": 8, "F": 14, "G": 21, "H": 1, "I": 39}
TEXT = "".join([x * y for x, y in FREQ.items()])
print("Original:\t", TEXT)

hf = Huffman()
enc, huff = hf.huffman_encoding(TEXT)
print("Huffman:\t", huff)
dec = hf.huffman_decoding(enc, huff)
print("Decoded:\t", dec)
print("Are they the same? ", TEXT == dec)
