from codegen import CodeGenerator
from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     START
#     PUSHI 10
#     STOREL 0
#     PUSHL 0
#     PUSHI 20
#     ADD
#     STOREL 1
#     PUSHL 1
#     WRITEI
#     WRITELN
#     STOP


# código do programa Pascal
code = """
program exemplo;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    writeln(y);
end.
"""

# gerar AST
ast = parser.parse(code)

# Verificar parsing
if not parser.success:
    print("❌ Erro de parsing — não é possível prosseguir")
else:

    # análise semântica
    analyzer = SemanticAnalyzer()
    ok = analyzer.analyze(ast)
    
    if not ok:
        print("❌ Erros semânticos detetados")
        analyzer.report_errors()
    else:
        
        # gerar código da VM
        generator = CodeGenerator(analyzer.symtab)
        instructions = generator.generate(ast)
        print(instructions)