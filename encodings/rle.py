'''
    Run-length encoding
    [https://en.wikipedia.org/wiki/Run-length_encoding]
'''


class E_RLE:

    def get_first_byte(self, data):
        if len(data) > 0:
            return data[0]

        return False

    def get_count(self):
        r = []

        while self.n > 0:
            k = min(255, self.n)
            r.append(k)
            r.append(self.byte)
            self.n -= k

        return r

    def encode(self, data):
        result = bytearray()
        self.byte = self.get_first_byte(data)
        self.n = 0

        for byte in data:
            if byte != self.byte:
                result.extend(self.get_count())
                self.byte = byte
                self.n = 0

            self.n += 1

        result.extend(self.get_count())

        return result

    def decode(self, data):
        result = bytearray()

        for i in range(0, len(data), 2):
            byte = data[i+1]
            for _ in range(data[i]):
                result.append(byte)

        return result


program = E_RLE()
