from lexer import lexer

# OUTPUT:
#     LexToken(PROGRAM,'program',2,1)
#     LexToken(ID,'SomaArray',2,9)
#     LexToken(PONTOEVIRG,';',2,18)
#     LexToken(VAR,'var',3,20)
#     LexToken(ID,'numeros',4,24)
#     LexToken(DOISPONTOS,':',4,31)
#     LexToken(ARRAY,'array',4,33)
#     LexToken(LBRACKET,'[',4,38)
#     LexToken(NUM,1,4,39)
#     LexToken(INTERVALO,'..',4,40)
#     LexToken(NUM,5,4,42)
#     LexToken(RBRACKET,']',4,43)
#     LexToken(OF,'of',4,45)
#     LexToken(INTEGER,'integer',4,48)
#     LexToken(PONTOEVIRG,';',4,55)
#     LexToken(ID,'i',5,57)
#     LexToken(VIRG,',',5,58)
#     LexToken(ID,'soma',5,60)
#     LexToken(DOISPONTOS,':',5,64)
#     LexToken(INTEGER,'integer',5,66)
#     LexToken(PONTOEVIRG,';',5,73)
#     LexToken(BEGIN,'begin',6,75)
#     LexToken(ID,'soma',7,81)
#     LexToken(ATRIBUICAO,':=',7,86)
#     LexToken(NUM,0,7,89)
#     LexToken(PONTOEVIRG,';',7,90)
#     LexToken(WRITELN,'writeln',8,92)
#     LexToken(LPAREN,'(',8,99)
#     LexToken(STRING,'Introduza 5 números inteiros:',8,100)
#     LexToken(RPAREN,')',8,131)
#     LexToken(PONTOEVIRG,';',8,132)
#     LexToken(FOR,'for',9,134)
#     LexToken(ID,'i',9,138)
#     LexToken(ATRIBUICAO,':=',9,140)
#     LexToken(NUM,1,9,143)
#     LexToken(TO,'to',9,145)
#     LexToken(NUM,5,9,148)
#     LexToken(DO,'do',9,150)
#     LexToken(BEGIN,'begin',10,153)
#     LexToken(READLN,'readln',11,159)
#     LexToken(LPAREN,'(',11,165)
#     LexToken(ID,'numeros',11,166)
#     LexToken(LBRACKET,'[',11,173)
#     LexToken(ID,'i',11,174)
#     LexToken(RBRACKET,']',11,175)
#     LexToken(RPAREN,')',11,176)
#     LexToken(PONTOEVIRG,';',11,177)
#     LexToken(ID,'soma',12,179)
#     LexToken(ATRIBUICAO,':=',12,184)
#     LexToken(ID,'soma',12,187)
#     LexToken(SOMA,'+',12,192)
#     LexToken(ID,'numeros',12,194)
#     LexToken(LBRACKET,'[',12,201)
#     LexToken(ID,'i',12,202)
#     LexToken(RBRACKET,']',12,203)
#     LexToken(PONTOEVIRG,';',12,204)
#     LexToken(END,'end',13,206)
#     LexToken(PONTOEVIRG,';',13,209)
#     LexToken(WRITELN,'writeln',14,211)
#     LexToken(LPAREN,'(',14,218)
#     LexToken(STRING,'A soma dos números é: ',14,219)
#     LexToken(VIRG,',',14,243)
#     LexToken(ID,'soma',14,245)
#     LexToken(RPAREN,')',14,249)
#     LexToken(PONTOEVIRG,';',14,250)
#     LexToken(END,'end',15,252)
#     LexToken(PONTO,'.',15,255)


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

lexer.input(code)

for tok in lexer:
    print(tok)
