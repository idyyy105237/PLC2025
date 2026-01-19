from codegen import CodeGenerator
from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     START
#     PUSHS "Introduza um número inteiro positivo:"
#     WRITES
#     WRITELN
#     READ
#     ATOI
#     STOREL 0
#     PUSHI 1
#     STOREL 2
#     PUSHI 1
#     STOREL 1
#     LOOP1:
#     PUSHL 1
#     PUSHL 0
#     INFEQ
#     JZ END2
#     PUSHL 2
#     PUSHL 1
#     MUL
#     STOREL 2
#     PUSHL 1
#     PUSHI 1
#     ADD
#     STOREL 1
#     JUMP LOOP1
#     END2:
#     PUSHS "Fatorial de "
#     WRITES
#     PUSHL 0
#     WRITEI
#     PUSHS ": "
#     WRITES
#     PUSHL 2
#     WRITEI
#     WRITELN
#     STOP


# código do programa Pascal
code = """
program Fatorial;
var
n, i, fat: integer;
begin
writeln('Introduza um número inteiro positivo:');
readln(n);
fat := 1;
for i := 1 to n do
fat := fat * i;
writeln('Fatorial de ', n, ': ', fat);
end.
"""

# gerar AST
ast = parser.parse(code)

# análise semântica
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# gerar código da VM
generator = CodeGenerator(analyzer.symtab)
instructions = generator.generate(ast)
print(instructions)