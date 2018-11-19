'''
    4B5B (4 bity na 5 bitů)
    [https://en.wikipedia.org/wiki/4B5B]
'''

ENC_TABLE = {
    0b0000: 0b11110, 0b0001: 0b01001, 0b0010: 0b10100, 0b0011: 0b10101,
    0b0100: 0b01010, 0b0101: 0b01011, 0b0110: 0b01110, 0b0111: 0b01111,
    0b1000: 0b10010, 0b1001: 0b10011, 0b1010: 0b10110, 0b1011: 0b10111,
    0b1100: 0b11010, 0b1101: 0b11011, 0b1110: 0b11100, 0b1111: 0b11101,
}
DEC_TABLE = {key: value for value, key in ENC_TABLE.items()}


class E_4B5B:

    def load_bits(self, n):
        r = []

        while self.length >= n:
            self.length -= n
            r.append(self.number >> self.length)
            self.number %= 1 << self.length

        return r

    def encode(self, data):
        result = bytearray()
        self.number = 0
        self.length = 0

        for byte in data:
            a = (byte & 0b11110000) >> 4
            b = (byte & 0b00001111) >> 0

            self.number = (self.number << 5) + ENC_TABLE[a]
            self.number = (self.number << 5) + ENC_TABLE[b]
            self.length += 10

            result.extend(self.load_bits(8))

        if self.length > 0:
            result.append(self.number << (8 - self.length))

        return result

    def decode(self, data):
        result = bytearray()
        self.number = 0
        self.length = 0

        for byte in data:
            self.number = (self.number << 8) + byte
            self.length += 8

            for n in self.load_bits(10):
                a = (n & 0b1111100000) >> 5
                b = (n & 0b0000011111) >> 0

                result.append((DEC_TABLE[a] << 4) + DEC_TABLE[b])

        return result


program = E_4B5B()
