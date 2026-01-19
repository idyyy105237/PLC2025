import ply.yacc as yacc
from lexer import tokens

# =====================================================================
#                              GRAMÁTICA
# =====================================================================
#
#  programa :
#        PROGRAM ID ; declaracoes bloco_final
#
#  bloco_final :
#        BEGIN comandos END .
#
# ---------------------------------------------------------------------
#  declaracoes :
#        VAR lista_declaracoes
#      | (vazio)
#
#  lista_declaracoes :
#        lista_declaracoes declaracao
#      | declaracao
#
#  declaracao :
#        lista_ids : tipo ;
#
#  lista_ids :
#        ID
#      | lista_ids , ID
#
#  tipo :
#        INTEGER
#      | REAL
#      | BOOLEAN
#      | STRING_TYPE
#      | ARRAY [ intervalo ] OF tipo
#
# =====================================================================
#  intervalo :
#        NUM .. NUM           (token INTERVALO)
#
# =====================================================================
#  comandos :
#        comandos comando
#      | comando
#
#  comando :
#        atribuicao
#      | atribuicao_array
#      | comando_if
#      | comando_while
#      | comando_for
#      | comando_writeln
#      | comando_readln
#      | bloco PONTOEVIRG     (bloco como comando normal)
#
#  bloco :
#        BEGIN comandos END
#
# =====================================================================
#  expr :
#        expr + expr
#      | expr - expr
#      | expr * expr
#      | expr / expr
#      | expr DIV expr
#      | expr MOD expr
#      | expr relop expr
#      | expr AND expr
#      | expr OR expr
#      | NOT expr
#      | -expr
#      | ( expr )
#      | NUM
#      | ID
#      | ID [ expr ]
#      | STRING
#      | TRUE
#      | FALSE
# =====================================================================

# ============================================================================
# PRECEDÊNCIA DOS OPERADORES (inclui dangling-else)
# ============================================================================
precedence = (
    ('right', 'NOT'),
    ('left', 'MULT', 'DIVIDE', 'DIV', 'MOD'),
    ('left', 'SOMA', 'SUBTR'),
    ('left', 'IGUAL', 'DIFF', 'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'NEG'),
    ('right', 'ELSE'),
)

# ============================================================================
# IMPLEMENTAÇÃO
# ============================================================================

def p_programa(p):
    'programa : PROGRAM ID PONTOEVIRG declaracoes bloco_final'
    p[0] = ('programa', p[2], p[4], p[5])

def p_bloco_final(p):
    'bloco_final : BEGIN comandos END PONTO'
    p[0] = ('bloco_principal', p[2])


# ---------------- DECLARAÇÕES ----------------

def p_declaracoes_var(p):
    'declaracoes : VAR lista_declaracoes'
    p[0] = p[2]

def p_declaracoes_vazio(p):
    'declaracoes :'
    p[0] = []

def p_lista_declaracoes_multi(p):
    'lista_declaracoes : lista_declaracoes declaracao'
    p[0] = p[1] + [p[2]]

def p_lista_declaracoes_single(p):
    'lista_declaracoes : declaracao'
    p[0] = [p[1]]

def p_declaracao(p):
    'declaracao : lista_ids DOISPONTOS tipo PONTOEVIRG'
    p[0] = ('decl', p[1], p[3])

def p_lista_ids_multi(p):
    'lista_ids : lista_ids VIRG ID'
    p[0] = p[1] + [p[3]]

def p_lista_ids_single(p):
    'lista_ids : ID'
    p[0] = [p[1]]

def p_tipo_base(p):
    '''tipo : INTEGER
            | REAL
            | BOOLEAN
            | STRING_TYPE'''
    p[0] = p[1]

def p_tipo_array(p):
    'tipo : ARRAY LBRACKET intervalo RBRACKET OF tipo'
    p[0] = ('array', p[3], p[6])

def p_intervalo(p):
    'intervalo : NUM INTERVALO NUM'
    p[0] = (p[1], p[3])


# ---------------- COMANDOS ----------------
# O ponto-e-vírgula é tratado aqui como SEPARADOR entre comandos.
# Também aceitamos um ';' final opcional antes do END.

def p_comandos_single(p):
    'comandos : comando'
    p[0] = [p[1]]

def p_comandos_multi(p):
    'comandos : comandos PONTOEVIRG comando'
    p[0] = p[1] + [p[3]]

def p_comandos_trailing_semicolon(p):
    'comandos : comandos PONTOEVIRG'
    # permite um ; final antes do END
    p[0] = p[1]

def p_comando(p):
    '''comando : atribuicao
               | atribuicao_array
               | comando_if
               | comando_while
               | comando_for
               | comando_writeln
               | comando_readln
               | bloco'''
    p[0] = p[1]


# ---------------- BLOCO BEGIN/END ----------------

def p_bloco(p):
    'bloco : BEGIN comandos END'
    p[0] = ('bloco', p[2])


# ---------------- ATRIBUIÇÃO ----------------
# NOTA: removido PONTOEVIRG daqui — ';' é tratado pela regra 'comandos'

def p_atribuicao(p):
    'atribuicao : ID ATRIBUICAO expr'
    p[0] = ('atribuicao', p[1], p[3])

def p_atribuicao_array(p):
    'atribuicao_array : ID LBRACKET expr RBRACKET ATRIBUICAO expr'
    p[0] = ('atribuicao_array', p[1], p[3], p[6])


# ---------------- IF ----------------
# Dangling-else resolvido pela precedência ('right','ELSE')

def p_comando_if(p):
    'comando_if : IF expr THEN comando'
    p[0] = ('if', p[2], p[4])

def p_comando_if_else(p):
    'comando_if : IF expr THEN comando ELSE comando'
    p[0] = ('ifelse', p[2], p[4], p[6])


# ---------------- WHILE ----------------

def p_comando_while(p):
    'comando_while : WHILE expr DO comando'
    p[0] = ('while', p[2], p[4])


# ---------------- FOR ----------------

def p_comando_for_to(p):
    'comando_for : FOR ID ATRIBUICAO expr TO expr DO comando'
    p[0] = ('for_to', p[2], p[4], p[6], p[8])

def p_comando_for_downto(p):
    'comando_for : FOR ID ATRIBUICAO expr DOWNTO expr DO comando'
    p[0] = ('for_down', p[2], p[4], p[6], p[8])


# ---------------- WRITELN ----------------
# removido PONTOEVIRG daqui

def p_comando_writeln(p):
    'comando_writeln : WRITELN LPAREN lista_expr RPAREN'
    p[0] = ('writeln', p[3])

def p_lista_expr_multi(p):
    'lista_expr : lista_expr VIRG expr'
    p[0] = p[1] + [p[3]]

def p_lista_expr_single(p):
    'lista_expr : expr'
    p[0] = [p[1]]


# ---------------- READLN ----------------
# removido PONTOEVIRG daqui

def p_comando_readln(p):
    'comando_readln : READLN LPAREN lista_expr RPAREN'
    p[0] = ('readln', p[3])


# ============================================================================
# EXPRESSÕES
# ============================================================================

def p_expr_binop(p):
    '''expr : expr SOMA expr
            | expr SUBTR expr
            | expr MULT expr
            | expr DIVIDE expr
            | expr DIV expr
            | expr MOD expr
            | expr IGUAL expr
            | expr DIFF expr
            | expr MAIOR expr
            | expr MENOR expr
            | expr MAIORIGUAL expr
            | expr MENORIGUAL expr
            | expr AND expr
            | expr OR expr'''
    p[0] = ('op', p[2], p[1], p[3])

def p_expr_not(p):
    'expr : NOT expr'
    p[0] = ('not', p[2])

def p_expr_neg(p):
    'expr : SUBTR expr %prec NEG'
    p[0] = ('neg', p[2])

def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_num(p):
    'expr : NUM'
    p[0] = ('num', p[1])

def p_expr_id(p):
    'expr : ID'
    p[0] = ('id', p[1])

def p_expr_array_access(p):
    'expr : ID LBRACKET expr RBRACKET'
    p[0] = ('array_access', p[1], p[3])

def p_expr_string(p):
    'expr : STRING'
    p[0] = ('string', p[1])

def p_expr_true(p):
    'expr : TRUE'
    p[0] = ('true',)

def p_expr_false(p):
    'expr : FALSE'
    p[0] = ('false',)


# =====================================================================
# ERROS
# =====================================================================
def p_error(p):
    if p:
        lineno = getattr(p, 'lineno', None)
        print(f"Erro de sintaxe na linha {lineno}: token '{p.type}' com valor '{p.value}'")
    else:
        print("Erro de sintaxe: fim inesperado do input")
    parser.success = False


parser = yacc.yacc()
parser.success = True