from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Expressões de início/fim do FOR devem ser integer (obtido: real, integer).


# ERRO: Limites do FOR não são inteiros

code = """
program Ex10;
var
    i: integer;
begin
    for i := 1.5 to 10 do   { ERRO: limites devem ser integer }
        writeln(i);
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
