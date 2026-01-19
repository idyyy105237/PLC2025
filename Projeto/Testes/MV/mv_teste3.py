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
#     PUSHI 2
#     STOREL 1
#     WHILE1:
#     PUSHL 1
#     PUSHL 0
#     PUSHI 2
#     DIV
#     INFEQ
#     PUSHL 2
#     AND
#     JZ END2
#     PUSHL 0
#     PUSHL 1
#     MOD
#     PUSHI 0
#     EQUAL
#     JZ ELSE3
#     PUSHI 0
#     STOREL 2
#     JUMP ENDIF4
#     ELSE3:
#     ENDIF4:
#     PUSHL 1
#     PUSHI 1
#     ADD
#     STOREL 1
#     JUMP WHILE1
#     END2:
#     PUSHL 2
#     JZ ELSE5
#     PUSHL 0
#     WRITEI
#     PUSHS " é um número primo"
#     WRITES
#     WRITELN
#     JUMP ENDIF6
#     ELSE5:
#     PUSHL 0
#     WRITEI
#     PUSHS " não é um número primo"
#     WRITES
#     WRITELN
#     ENDIF6:
#     STOP


# código do programa Pascal
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

# gerar AST
ast = parser.parse(code)

# análise semântica
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# gerar código da VM
generator = CodeGenerator(analyzer.symtab)
instructions = generator.generate(ast)
print(instructions)