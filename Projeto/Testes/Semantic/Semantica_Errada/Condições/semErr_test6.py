from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Condição do IF deve ser boolean, obteve 'integer'.


# ERRO: Condição do IF não é boolean

code = """
program Ex6;
var
    x: integer;
begin
    x := 10;
    if x then   { ERRO: IF exige boolean }
        writeln('ok');
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
