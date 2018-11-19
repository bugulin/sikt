'''
    Lempel–Ziv–Welch algoritmus
    [https://en.wikipedia.org/wiki/Lempel–Ziv–Welch]

    * nefunguje pro všechny znaky, ale alespoň pro delší vstup
'''

from main import ENCODING

# Pokud bude abeceda až moc rozsáhlá, zakódované číslo se nevejde do 1 bytu
ALPHABET = range(13, 200)


class E_LZW:

    def encode(self, data):
        result = bytearray()
        dictionary = {
            bytes([letter]): index
            for index, letter in enumerate(ALPHABET)
        }
        counter = len(dictionary)
        index = 0

        length = len(data)
        data.append(0)
        while index < length:
            phrase = bytearray([data[index]])

            while bytes(phrase) in dictionary.keys():
                index += 1
                phrase.append(data[index])

            phrase = bytes(phrase)
            dictionary[phrase] = counter
            counter += 1
            result.append(dictionary[phrase[:-1]])

        return result

    def decode(self, data):
        result = bytearray()
        dictionary = [bytes([letter]) for letter in ALPHABET]
        prev = None

        for byte in data:
            try:
                phrase = dictionary[byte]
            except IndexError:
                phrase = prev + bytes([prev[0]])

            result.extend(phrase)
            if prev is not None:
                dictionary.append(prev + bytes([phrase[0]]))
            prev = phrase

        return result


program = E_LZW()
