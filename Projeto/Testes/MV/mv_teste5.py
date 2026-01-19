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

(*
   comentário
*)

program exemplo;
var x, y: integer;

//isto aqui tambem é um comentario
begin
    x := 10;
    { isto é um 
    comentário
    }
    y := x + 20;
    writeln(y);
(*
   comentário
*)
end.

(*
   comentário
*)

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