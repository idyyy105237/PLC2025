from lexer import lexer

# OUTPUT:
#     LexToken(PROGRAM,'program',2,1)
#     LexToken(ID,'exemplo',2,9)
#     LexToken(PONTOEVIRG,';',2,16)
#     LexToken(VAR,'var',3,18)
#     LexToken(ID,'x',3,22)
#     LexToken(VIRG,',',3,23)
#     LexToken(ID,'y',3,25)
#     LexToken(DOISPONTOS,':',3,26)
#     LexToken(INTEGER,'integer',3,28)
#     LexToken(PONTOEVIRG,';',3,35)
#     LexToken(BEGIN,'begin',4,37)
#     LexToken(ID,'x',5,47)
#     LexToken(ATRIBUICAO,':=',5,49)
#     LexToken(NUM,10,5,52)
#     LexToken(PONTOEVIRG,';',5,54)
#     LexToken(ID,'y',6,60)
#     LexToken(ATRIBUICAO,':=',6,62)
#     LexToken(ID,'x',6,65)
#     LexToken(SOMA,'+',6,67)
#     LexToken(NUM,20,6,69)
#     LexToken(PONTOEVIRG,';',6,71)
#     LexToken(WRITELN,'writeln',7,77)
#     LexToken(LPAREN,'(',7,84)
#     LexToken(ID,'y',7,85)
#     LexToken(RPAREN,')',7,86)
#     LexToken(PONTOEVIRG,';',7,87)
#     LexToken(END,'end',8,89)
#     LexToken(PONTO,'.',8,92)


code = """
program exemplo;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    writeln(y);
end.

"""

lexer.input(code)

for tok in lexer:
    print(tok)
