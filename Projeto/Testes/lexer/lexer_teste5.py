from lexer import lexer

# OUTPUT:
#    LexToken(PROGRAM,'program',7,23)
#    LexToken(ID,'exemplo',7,31)
#    LexToken(PONTOEVIRG,';',7,38)
#    LexToken(VAR,'var',8,40)
#    LexToken(ID,'x',8,44)
#    LexToken(VIRG,',',8,45)
#    LexToken(ID,'y',8,47)
#    LexToken(DOISPONTOS,':',8,48)
#    LexToken(INTEGER,'integer',8,50)
#    LexToken(PONTOEVIRG,';',8,57)
#    LexToken(BEGIN,'begin',11,95)
#    LexToken(ID,'x',12,105)
#    LexToken(ATRIBUICAO,':=',12,107)
#    LexToken(NUM,10,12,110)
#    LexToken(PONTOEVIRG,';',12,112)
#    LexToken(ID,'y',16,156)
#    LexToken(ATRIBUICAO,':=',16,158)
#    LexToken(ID,'x',16,161)
#    LexToken(SOMA,'+',16,163)
#    LexToken(NUM,20,16,165)
#    LexToken(PONTOEVIRG,';',16,167)
#    LexToken(WRITELN,'writeln',17,173)
#    LexToken(LPAREN,'(',17,180)
#    LexToken(ID,'y',17,181)
#    LexToken(RPAREN,')',17,182)
#    LexToken(PONTOEVIRG,';',17,183)
#    LexToken(END,'end',21,205)
#    LexToken(PONTO,'.',21,208)


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

lexer.input(code)

for tok in lexer:
    print(tok)