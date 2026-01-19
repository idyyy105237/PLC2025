from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Atribuição a variável não declarada 'y'.
#     - Incompatibilidade de tipos na atribuição a 'x': variável é 'real' mas expressão é 'array'.
#     - Índice do array 'arr' deve ser integer, obteve 'real'.
#     - Condição do IF deve ser boolean, obteve 'real'.


# ERRO: Vários erros

code = """
program Ex18;
var
    x: real;
    arr: array[1..3] of boolean;
begin
    y := 10;                { y não declarado }
    x := arr;               { tipos incompatíveis }
    arr[1.5] := true;       { índice não-inteiro }
    if x then writeln('x'); { condição não-boolean }
end.
"""

# ---------------------------------------
# Gerar AST
# ---------------------------------------

ast = parser.parse(code)

# ---------------------------------------
# Executar análise semântica
# ---------------------------------------

analyzer = SemanticAnalyzer()
ok = analyzer.analyze(ast)

# ---------------------------------------
# Resultado final
# ---------------------------------------

if ok:
    print("✅ Semântica correta — nenhum erro encontrado.")
else:
    print("❌ Erros semânticos detetados:\n")
    analyzer.report_errors()
