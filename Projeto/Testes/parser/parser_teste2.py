from parser import parser

# OUTPUT:
#     ('programa', 'Fatorial', 
#     [('decl', ['n', 'i', 'fat'], 'integer')], 
#     ('bloco_principal', 
#         [('writeln', 
#         [('string', 'Introduza um número inteiro positivo:')]), 
#         ('readln', [('id', 'n')]), 
#         ('atribuicao', 'fat', ('num', 1)), 
#         ('for_to', 'i', ('num', 1), ('id', 'n'), 
#         ('atribuicao', 'fat', ('op', '*', ('id', 'fat'), ('id', 'i')))), 
#         ('writeln', [('string', 'Fatorial de '), ('id', 'n'), ('string', ': '), ('id', 'fat')])]))


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

result = parser.parse(code)

if parser.success:
    print(result)
else:
    print("❌ Parsing falhou — AST não foi gerado")