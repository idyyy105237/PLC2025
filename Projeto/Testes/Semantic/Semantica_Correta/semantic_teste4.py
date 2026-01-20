from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ✅ Semântica correta — nenhum erro encontrado.


code = """
program SomaArray;
var
numeros: array[1..5] of integer;
i, soma: integer;
begin
soma := 0;
writeln('Introduza 5 números inteiros:');
for i := 1 to 5 do
begin
readln(numeros[i]);
soma := soma + numeros[i];
end;
writeln('A soma dos números é: ', soma);
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