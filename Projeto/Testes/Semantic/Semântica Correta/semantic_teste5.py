from parser import parser
from semantic import SemanticAnalyzer

# OUTPUT:
#     ✅ Semântica correta — nenhum erro encontrado.


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