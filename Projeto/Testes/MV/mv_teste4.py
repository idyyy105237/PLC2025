from codegen import CodeGenerator
from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     START
#     PUSHI 0
#     STOREL 6
#     PUSHS "Introduza 5 números inteiros:"
#     WRITES
#     WRITELN
#     PUSHI 1
#     STOREL 5
#     LOOP1:
#     PUSHL 5
#     PUSHI 5
#     INFEQ
#     JZ END2
#     PUSHFP
#     PUSHI 0
#     PADD
#     PUSHL 5
#     PUSHI 1
#     SUB
#     PADD
#     READ
#     ATOI
#     STORE 0
#     PUSHL 6
#     PUSHFP
#     PUSHI 0
#     PADD
#     PUSHL 5
#     PUSHI 1
#     SUB
#     PADD
#     LOAD 0
#     ADD
#     STOREL 6
#     PUSHL 5
#     PUSHI 1
#     ADD
#     STOREL 5
#     JUMP LOOP1
#     END2:
#     PUSHS "A soma dos números é: "
#     WRITES
#     PUSHL 6
#     WRITEI
#     WRITELN
#     STOP


# código do programa Pascal
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

# gerar AST
ast = parser.parse(code)

# análise semântica
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# gerar código da VM
generator = CodeGenerator(analyzer.symtab)
instructions = generator.generate(ast)
print(instructions)