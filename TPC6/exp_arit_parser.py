#Gramatica
"""
S         -> Literal MaisMenos
MaisMenos -> '+' Literal MaisMenos | '-' Literal MaisMenos | ε
Literal   -> Fator MultDiv
MultDiv   -> '*' Fator MultDiv | '/' Fator MultDiv | ε
Fator     -> Int | '(' S ')'

"""

from exp_arit_lexer import lexer

token = None

def proximo():
    global token
    token = lexer.token()

def espera(tipo):
    if token and token.type == tipo:
        proximo()
    else:
        raise ValueError(f"Esperava {tipo}, encontrei {token.value if token else None}")

# -------------------
# Funções do parser
# -------------------

def S():
    Literal()
    MaisMenos()

def MaisMenos():
    if token and token.type in ("ADD", "SUB"):
        operador = token.type
        espera(operador)
        Literal()
        MaisMenos()

def Literal():
    Fator()
    MultDiv()

def MultDiv():
    if token and token.type in ("MUL", "DIV"):
        operador = token.type
        espera(operador)
        Fator()
        MultDiv()

def Fator():
    if token and token.type == "INT":
        espera("INT")
    elif token and token.type == "PA":
        espera("PA")
        S()
        espera("PF")
    else:
        raise ValueError(f"Token inesperado: {token.value if token else None}")

# -------------------
# Ponto de entrada
# -------------------

def analisar(expr):
    global token
    lexer.input(expr)
    proximo()
    S()
    if token is not None:
        raise ValueError(f"Símbolos restantes após análise: {token}")
    return "Expressão válida ✅"

print(analisar("5+6"))
print(analisar("(7-2)*(8/3)"))
print(analisar("(3-7)"))
print(analisar("3+2*5"))
print(analisar("(3-7)*2"))
print(analisar("(3-7)/2"))