from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     Erro de sintaxe na linha 4: token 'ID' com valor 'inteiro'
#     ❌ Erros semânticos detetados:

#     Erros semânticos encontrados:
#     - AST inválida: nó raiz não é 'programa'.



# ERRO: Atribuição para tipo desconhecido

code = """
program Ex16;
var
    x: inteiro;   { ERRO: tipo não existe }
begin
    x := 5;
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
