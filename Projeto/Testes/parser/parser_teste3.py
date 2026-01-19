from parser import parser

# OUTPUT:
#     ('programa', 'NumeroPrimo', 
#     [('decl', ['num', 'i'], 'integer'), 
#     ('decl', ['primo'], 'boolean')], 
#     ('bloco_principal', 
#         [('writeln', [('string', 'Introduza um número inteiro positivo:')]), 
#         ('readln', [('id', 'num')]), 
#         ('atribuicao', 'primo', ('true',)), 
#         ('atribuicao', 'i', ('num', 2)), 
#         ('while', ('op', 'and', ('op', '<=', ('id', 'i'), ('op', 'div', ('id', 'num'), ('num', 2))), ('id', 'primo')), 
#         ('bloco', 
#             [('if', ('op', '=', ('op', 'mod', ('id', 'num'), ('id', 'i')), ('num', 0)), 
#             ('atribuicao', 'primo', ('false',))), 
#             ('atribuicao', 'i', ('op', '+', ('id', 'i'), ('num', 1)))])), 
#         ('ifelse', ('id', 'primo'), 
#             ('writeln', [('id', 'num'), ('string', ' é um número primo')]), 
#             ('writeln', [('id', 'num'), ('string', ' não é um número primo')]))]))


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

result = parser.parse(code)

if parser.success:
    print(result)
else:
    print("❌ Parsing falhou — AST não foi gerado")