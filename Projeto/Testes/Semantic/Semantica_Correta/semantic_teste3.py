from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ✅ Semântica correta — nenhum erro encontrado.


code = """
program NumeroPrimo;
    var
        num, i: integer;
        primo: boolean;
    begin
        writeln('Introduza um número inteiro positivo:');
        readln(num);
        primo := true;
        i := 2;
        while (i <= (num div 2)) and primo do
        begin
            if (num mod i) = 0 then
            primo := false;
            i := i + 1;
        end;
        if primo then
        writeln(num, ' é um número primo')
        else
        writeln(num, ' não é um número primo')
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
