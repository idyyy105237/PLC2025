from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - Operador '+' exige operandos numéricos (integer/real). Obteve: 'integer' e 'string'.


# ERRO: Operação aritmética entre tipos incompatíveis

code = """
program Ex4;
var
    s: string;
    x: integer;
begin
    s := 'ola';
    x := 5 + s;   { ERRO: não pode somar string com integer }
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
