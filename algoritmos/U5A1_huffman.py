from heapq import heappush, heappop, heapify
from collections import defaultdict


def huffman_encoding(text: str) -> tuple:
    # Paso 1: Contar las frecuencias de cada caracter en la cadena de entrada
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    # Paso 2: Construir el árbol de Huffman
    # utilizando una cola de prioridad (heap)
    heap = [[wt, [sym, ""]] for sym, wt in freq.items()]
    heapify(heap)

    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Paso 3: Crear un diccionario que asocie cada
    # caracter con su código de Huffman
    huffman_dict = dict(heappop(heap)[1:])

    # Paso 4: Codificar la cadena de entrada
    # utilizando el diccionario de Huffman
    encoded = ""
    for char in text:
        encoded += huffman_dict[char]

    return encoded, huffman_dict


def huffman_decoding(encoded, huffman_dict):
    # Invertir el diccionario de Huffman para poder
    # decodificar la cadena de entrada
    inv_dict = {v: k for k, v in huffman_dict.items()}

    # Decodificar la cadena de entrada utilizando
    # el diccionario invertido
    decoded = ""
    code = ""
    for bit in encoded:
        code += bit
        if code in inv_dict:
            decoded += inv_dict[code]
            code = ""

    return decoded


FREQ = {"A": 5, "B": 12, "C": 35, "D": 3, "E": 8, "F": 14, "G": 21, "H": 1, "I": 39}
TEXT = "".join([x * y for x, y in FREQ.items()])
print("Original:\t", TEXT)

enc, huff = huffman_encoding(TEXT)
dec = huffman_decoding(enc, huff)
print("Huffman:\t", dec)
print("Are they the same? ", TEXT==dec)
