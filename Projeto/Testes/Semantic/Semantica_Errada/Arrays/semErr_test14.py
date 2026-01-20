from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Índice 1 fora dos limites do array 'arr' [2..4].


# ERRO: Índice literal fora dos limites

code = """
program Ex14;
var
    arr: array[2..4] of integer;
begin
    arr[1] := 5;   { ERRO: 1 está fora de 2..4 }
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
