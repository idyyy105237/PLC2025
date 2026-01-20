from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Incompatibilidade de tipos na atribuição a 'x': variável é 'integer' mas expressão é 'boolean'.



# ERRO: Atribuição com tipos incompatíveis

code = """
program Ex3;
var
    x: integer;
begin
    x := true;   { ERRO: tipos incompatíveis }
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
