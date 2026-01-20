from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ✅ Semântica correta — nenhum erro encontrado.


code = """
program exemplo;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    writeln(y);
end.

"""

# ---------------------------------------
# Gerar AST
# ---------------------------------------

ast = parser.parse(code)

# ---------------------------------------
# Executar análise semântica
# ---------------------------------------

if not parser.success:
    print("❌ Erro de parsing — não é possível prosseguir com análise semântica")
else:
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
