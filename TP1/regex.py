#`regex.py` (programa em Python)
import re

# Expressão regular
pattern = re.compile(r'^(?:(?!011)[01])+$')

def valida(s):
    return bool(pattern.match(s))

if __name__ == "__main__":
    # Lê o ficheiro de testes
    with open("teste.txt") as f:
        casos = [linha.strip() for linha in f if linha.strip()]

    for s in casos:
        print(f"{s:25} -> {valida(s)}")
