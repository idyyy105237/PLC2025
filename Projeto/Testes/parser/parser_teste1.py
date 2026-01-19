from parser import parser

# OUTPUT:
#       ('programa', 'exemplo', 
#          [('decl', ['x', 'y'], 'integer')], 
#          ('bloco_principal', 
#            [('atribuicao', 'x', ('num', 10)), ('atribuicao', 'y', ('op', '+', ('id', 'x'), ('num', 20))), 
#             ('writeln', [('id', 'y')])]))


code = """
program exemplo;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    writeln(y);
end.

"""

result = parser.parse(code)

if parser.success:
    print(result)
else:
    print("❌ Parsing falhou — AST não foi gerado")