import ply.lex as lex

# -------------------------
# PALAVRAS-CHAVE
# -------------------------

reserved = {
    # ínicio do programa 
    'program': 'PROGRAM',
    
    # declaração de variáveis
    'var': 'VAR',
    
    # tipo: INTEGER
    'integer': 'INTEGER',
    
    # tipo: REAL
    'real': 'REAL',
    
    # tipo: BOOLEAN
    'boolean': 'BOOLEAN',
    
    # tipo: STRING
    'string': 'STRING_TYPE',
    
    # declaração de ínicio do programa
    'begin': 'BEGIN',
    
    # declaração de fim do programa
    'end': 'END',
    
    # condicional: IF
    'if': 'IF',
    
    # condicional: THEN
    'then': 'THEN',
    
    # condicional: ELSE
    'else': 'ELSE',
    
    # condicional: WHILE
    'while': 'WHILE',
    
    # condicional: DO
    'do': 'DO',
    
    # condicional: FOR
    'for': 'FOR',
    
    # condicional: TO
    'to': 'TO',
    
    # condicional: DOWNTO
    'downto': 'DOWNTO',
    
    # 'função': readln
    'readln': 'READLN',
    
    # 'função': readln
    'writeln': 'WRITELN',
    
    # 'função': mod
    'mod': 'MOD',
    
    # 'função': div
    'div': 'DIV', 
    
    # boleano True
    'true': 'TRUE',
    
    # boleano False
    'false': 'FALSE',
    
    # operador and
    'and': 'AND',
    
    # operador or
    'or': 'OR',
    
    # operador not
    'not': 'NOT',
    
    # arrays
    'array': 'ARRAY',
    'of': 'OF'

}



# -------------------------
# LISTA DE TOKENS
# -------------------------

tokens = (
    # TIPOS
    'INTEGER', 'REAL', 'BOOLEAN', 'STRING_TYPE',
    'NUM', 'ID', 'STRING', 
    'TRUE', 'FALSE', 'AND', 'OR', 'NOT',

    # PALAVRAS-CHAVE
    'PROGRAM', 'VAR', 'BEGIN', 'END',
    'IF', 'THEN', 'ELSE',
    'WHILE', 'DO',
    'FOR', 'TO', 'DOWNTO',
    'WRITELN', 'READLN',
    'ARRAY', 'OF', 'INTERVALO',

    # OPERADORES ARITMÉTICOS: +, -, *, / , div, mod
    'SOMA', 'SUBTR', 'MULT', 'DIVIDE', 'DIV', 'MOD',

    # OPERADORES LÓGICOS
    'IGUAL', 'DIFF', 'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL',

    # ATRIBUIÇÃO
    'ATRIBUICAO',

    # OUTROS
    'PONTOEVIRG', 'DOISPONTOS', 'VIRG', 'PONTO',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET'
)

# TOKENS SIMPLES

t_SOMA  = r'\+'
t_SUBTR = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'


t_MAIORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_DIFF = r'<>'
t_MAIOR = r'>'
t_MENOR = r'<'
t_IGUAL = r'='


t_ATRIBUICAO = r':='

t_INTERVALO = r'\.\.'

t_PONTOEVIRG = r';'
t_DOISPONTOS = r':'
t_VIRG = r','
t_PONTO = r'\.'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


# -------------------------
# TOKENS COMPLEXOS
# -------------------------

# STRINGS
def t_STRING(t):
    r'\'([^\\\']|\\.)*\''
    t.value = t.value[1:-1]   # remove as aspas
    return t


# NÚMEROS
def t_NUM(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# ID
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID') # diferencia palavras reservadas
    return t


# -------------------------
# COMENTÁRIOS
# -------------------------

# comentário multilinha do tipo  { ... }
def t_COMMENT1(t):
    r'\{[\s\S]*?\}'
    t.lexer.lineno += t.value.count('\n')

# comentário multilinha do tipo  (* ... *)
def t_COMMENT2(t):
    r'\(\*[\s\S]*?\*\)'
    t.lexer.lineno += t.value.count('\n')

# comentário do tipo // linha
def t_COMMENT(t):
    r'//.*'
    pass


# -------------------------
# CONTAGEM DE LINHAS
# -------------------------

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# -------------------------
# CARACTERES A IGNORAR
# -------------------------

t_ignore = ' \t'


# -------------------------
# ERROS LÉXICOS
# -------------------------

def t_error(t):
    print(f"Erro léxico: caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# -------------------------
# CRIAÇÃO DO LEXER
# -------------------------

lexer = lex.lex()