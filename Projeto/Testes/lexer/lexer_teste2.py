from lexer import lexer

# OUTPUT:
#     LexToken(PROGRAM,'program',2,1)
#     LexToken(ID,'Fatorial',2,9)
#     LexToken(PONTOEVIRG,';',2,17)
#     LexToken(VAR,'var',3,19)
#     LexToken(ID,'n',4,23)
#     LexToken(VIRG,',',4,24)
#     LexToken(ID,'i',4,26)
#     LexToken(VIRG,',',4,27)
#     LexToken(ID,'fat',4,29)
#     LexToken(DOISPONTOS,':',4,32)
#     LexToken(INTEGER,'integer',4,34)
#     LexToken(PONTOEVIRG,';',4,41)
#     LexToken(BEGIN,'begin',5,43)
#     LexToken(WRITELN,'writeln',6,49)
#     LexToken(LPAREN,'(',6,56)
#     LexToken(STRING,'Introduza um número inteiro positivo:',6,57)
#     LexToken(RPAREN,')',6,96)
#     LexToken(PONTOEVIRG,';',6,97)
#     LexToken(READLN,'readln',7,99)
#     LexToken(LPAREN,'(',7,105)
#     LexToken(ID,'n',7,106)
#     LexToken(RPAREN,')',7,107)
#     LexToken(PONTOEVIRG,';',7,108)
#     LexToken(ID,'fat',8,110)
#     LexToken(ATRIBUICAO,':=',8,114)
#     LexToken(NUM,1,8,117)
#     LexToken(PONTOEVIRG,';',8,118)
#     LexToken(FOR,'for',9,120)
#     LexToken(ID,'i',9,124)
#     LexToken(ATRIBUICAO,':=',9,126)
#     LexToken(NUM,1,9,129)
#     LexToken(TO,'to',9,131)
#     LexToken(ID,'n',9,134)
#     LexToken(DO,'do',9,136)
#     LexToken(ID,'fat',10,139)
#     LexToken(ATRIBUICAO,':=',10,143)
#     LexToken(ID,'fat',10,146)
#     LexToken(MULT,'*',10,150)
#     LexToken(ID,'i',10,152)
#     LexToken(PONTOEVIRG,';',10,153)
#     LexToken(WRITELN,'writeln',11,155)
#     LexToken(LPAREN,'(',11,162)
#     LexToken(STRING,'Fatorial de ',11,163)
#     LexToken(VIRG,',',11,177)
#     LexToken(ID,'n',11,179)
#     LexToken(VIRG,',',11,180)
#     LexToken(STRING,': ',11,182)
#     LexToken(VIRG,',',11,186)
#     LexToken(ID,'fat',11,188)
#     LexToken(RPAREN,')',11,191)
#     LexToken(PONTOEVIRG,';',11,192)
#     LexToken(END,'end',12,194)
#     LexToken(PONTO,'.',12,197)


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

lexer.input(code)

for tok in lexer:
    print(tok)
