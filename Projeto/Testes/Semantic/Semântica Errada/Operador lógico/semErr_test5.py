from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Operador lógico 'and' exige operandos boolean (obtido 'integer' e 'integer').
#     - Condição do IF deve ser boolean, obteve 'None'.


# ERRO: Utilização de operador lógico com operandos não-booleanos

code = """
program Ex5;
var
    x, y: integer;
begin
    x := 3;
    y := 4;
    if x and y then   { ERRO: and só aceita boolean }
        writeln('OK');
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
