from lexer import lexer

# OUTPUT:
#     LexToken(PROGRAM,'program',2,1)
#     LexToken(ID,'NumeroPrimo',2,9)
#     LexToken(PONTOEVIRG,';',2,20)
#     LexToken(VAR,'var',3,26)
#     LexToken(ID,'num',4,38)
#     LexToken(VIRG,',',4,41)
#     LexToken(ID,'i',4,43)
#     LexToken(DOISPONTOS,':',4,44)
#     LexToken(INTEGER,'integer',4,46)
#     LexToken(PONTOEVIRG,';',4,53)
#     LexToken(ID,'primo',5,63)
#     LexToken(DOISPONTOS,':',5,68)
#     LexToken(BOOLEAN,'boolean',5,70)
#     LexToken(PONTOEVIRG,';',5,77)
#     LexToken(BEGIN,'begin',6,83)
#     LexToken(WRITELN,'writeln',7,97)
#     LexToken(LPAREN,'(',7,104)
#     LexToken(STRING,'Introduza um número inteiro positivo:',7,105)
#     LexToken(RPAREN,')',7,144)
#     LexToken(PONTOEVIRG,';',7,145)
#     LexToken(READLN,'readln',8,155)
#     LexToken(LPAREN,'(',8,161)
#     LexToken(ID,'num',8,162)
#     LexToken(RPAREN,')',8,165)
#     LexToken(PONTOEVIRG,';',8,166)
#     LexToken(ID,'primo',9,176)
#     LexToken(ATRIBUICAO,':=',9,182)
#     LexToken(TRUE,'true',9,185)
#     LexToken(PONTOEVIRG,';',9,189)
#     LexToken(ID,'i',10,199)
#     LexToken(ATRIBUICAO,':=',10,201)
#     LexToken(NUM,2,10,204)
#     LexToken(PONTOEVIRG,';',10,205)
#     LexToken(WHILE,'while',11,215)
#     LexToken(LPAREN,'(',11,221)
#     LexToken(ID,'i',11,222)
#     LexToken(MENORIGUAL,'<=',11,224)
#     LexToken(LPAREN,'(',11,227)
#     LexToken(ID,'num',11,228)
#     LexToken(DIV,'div',11,232)
#     LexToken(NUM,2,11,236)
#     LexToken(RPAREN,')',11,237)
#     LexToken(RPAREN,')',11,238)
#     LexToken(AND,'and',11,240)
#     LexToken(ID,'primo',11,244)
#     LexToken(DO,'do',11,250)
#     LexToken(BEGIN,'begin',12,261)
#     LexToken(IF,'if',13,279)
#     LexToken(LPAREN,'(',13,282)
#     LexToken(ID,'num',13,283)
#     LexToken(MOD,'mod',13,287)
#     LexToken(ID,'i',13,291)
#     LexToken(RPAREN,')',13,292)
#     LexToken(IGUAL,'=',13,294)
#     LexToken(NUM,0,13,296)
#     LexToken(THEN,'then',13,298)
#     LexToken(ID,'primo',14,315)
#     LexToken(ATRIBUICAO,':=',14,321)
#     LexToken(FALSE,'false',14,324)
#     LexToken(PONTOEVIRG,';',14,329)
#     LexToken(ID,'i',15,343)
#     LexToken(ATRIBUICAO,':=',15,345)
#     LexToken(ID,'i',15,348)
#     LexToken(SOMA,'+',15,350)
#     LexToken(NUM,1,15,352)
#     LexToken(PONTOEVIRG,';',15,353)
#     LexToken(END,'end',16,363)
#     LexToken(PONTOEVIRG,';',16,366)
#     LexToken(IF,'if',17,376)
#     LexToken(ID,'primo',17,379)
#     LexToken(THEN,'then',17,385)
#     LexToken(WRITELN,'writeln',18,398)
#     LexToken(LPAREN,'(',18,405)
#     LexToken(ID,'num',18,406)
#     LexToken(VIRG,',',18,409)
#     LexToken(STRING,' é um número primo',18,411)
#     LexToken(RPAREN,')',18,431)
#     LexToken(ELSE,'else',19,441)
#     LexToken(WRITELN,'writeln',20,454)
#     LexToken(LPAREN,'(',20,461)
#     LexToken(ID,'num',20,462)
#     LexToken(VIRG,',',20,465)
#     LexToken(STRING,' não é um número primo',20,467)
#     LexToken(RPAREN,')',20,491)
#     LexToken(END,'end',21,497)
#     LexToken(PONTO,'.',21,500)


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

lexer.input(code)

for tok in lexer:
    print(tok)
