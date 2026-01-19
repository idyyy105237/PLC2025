from parser import parser

# OUTPUT:
#     ('programa', 'SomaArray', 
#     [('decl', ['numeros'], ('array', (1, 5), 'integer')), 
#     ('decl', ['i', 'soma'], 'integer')], 
#     ('bloco_principal', 
#         [('atribuicao', 'soma', ('num', 0)), 
#         ('writeln', [('string', 'Introduza 5 números inteiros:')]), 
#         ('for_to', 'i', ('num', 1), ('num', 5), 
#         ('bloco', 
#         [('readln', [('array_access', 'numeros', ('id', 'i'))]), 
#         ('atribuicao', 'soma', ('op', '+', ('id', 'soma'), ('array_access', 'numeros', ('id', 'i'))))])), 
#         ('writeln', [('string', 'A soma dos números é: '), ('id', 'soma')])]))


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

result = parser.parse(code)

if parser.success:
    print(result)
else:
    print("❌ Parsing falhou — AST não foi gerado")