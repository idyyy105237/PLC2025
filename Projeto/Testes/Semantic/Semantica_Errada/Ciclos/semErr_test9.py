from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Variável de controlo do FOR 'b' deve ser integer.
#     - Expressões de início/fim do FOR devem ser integer (obtido: boolean, boolean).

# ERRO: FOR com variável não-inteira

code = """
program Ex9;
var
    b: boolean;
begin
    for b := true to false do   { ERRO: controle do for deve ser integer }
        writeln('oi');
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
