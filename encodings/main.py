#!/usr/bin/env python3
import importlib
import importlib.util
from sys import argv, stderr, modules

ENCODING = 'utf-8'
REPORT = '''\
Vstup:              {}
Výstup:             {}
Úspěšné dekódování: {}
Kompresní poměr:    {:.2f}\
'''


class Program:

    def __init__(self, args):
        if len(args) > 1:
            self.path = argv[1:]
        else:
            self.path = [input('Zadejte jméno zdrojového souboru: ')]

    def load_module(self, path):
        self.spec = importlib.util.spec_from_file_location('program', path)
        if self.spec is None:
            print('[!] Program se nepodařilo načíst', file=stderr)
            return False

        self.module = importlib.util.module_from_spec(self.spec)
        self.spec.loader.exec_module(self.module)

        return True

    def execute(self):
        # Kódování dat
        self.spec.loader.exec_module(self.module)
        encoded = self.module.program.encode(self.text.copy())

        # Dekódování + znovu načtení modulu (kvůli vymazání paměti)
        self.spec.loader.exec_module(self.module)
        decoded = self.module.program.decode(encoded.copy())

        print(REPORT.format(
            self.to_binary(self.text),
            self.to_binary(encoded),
            ('✗', '✔')[self.text == decoded],
            len(self.text) / (len(encoded) or 1),
        ))

    def to_binary(self, text):
        result = []

        for char in text:
            result.append('{:08b}'.format(char))

        return ' '.join(result)

    def run(self):
        self.text = bytearray(input('Zadejte vstupní text: ').encode(ENCODING))

        for path in self.path:
            print('\n{:-^40}'.format(' {} '.format(path)))

            if self.load_module(path):
                try:
                    self.execute()
                except Exception as exc:
                    print('[!] Chyba ve spouštění: {}'.format(exc),
                          file=stderr)


if __name__ == '__main__':
    p = Program(argv)
    p.run()
