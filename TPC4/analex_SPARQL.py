
import sys
import re

def tokenize(input_string):
    reconhecidos = []
    mo = re.finditer(r'(?P<COMMENT>\#[^\n]*)|(?P<SELECT>select)|(?P<WHERE>where)|(?P<LIMIT>LIMIT)|(?P<RDFTYPE>\ba\b)|(?P<VAR>\?[a-zA-Z]\w*)|(?P<LITERAL>"[^"]*"(@[a-z]{2})?)|(?P<URI>[a-zA-Z_]\w*:[a-zA-Z_]\w*)|(?P<INT>\d+)|(?P<ABRE_CHAVES>\{)|(?P<FECHA_CHAVES>\})|(?P<PONTO>\.)|(?P<SKIP>[ \t])|(?P<NEWLINE>\n)|(?P<ERRO>.)', input_string)
    for m in mo:
        dic = m.groupdict()
        if dic['COMMENT']:
            t = ("COMMENT", dic['COMMENT'], nlinha, m.span())

        elif dic['SELECT']:
            t = ("SELECT", dic['SELECT'], nlinha, m.span())
    
        elif dic['WHERE']:
            t = ("WHERE", dic['WHERE'], nlinha, m.span())
    
        elif dic['LIMIT']:
            t = ("LIMIT", dic['LIMIT'], nlinha, m.span())
    
        elif dic['RDFTYPE']:
            t = ("RDFTYPE", dic['RDFTYPE'], nlinha, m.span())
    
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], nlinha, m.span())
    
        elif dic['LITERAL']:
            t = ("LITERAL", dic['LITERAL'], nlinha, m.span())
    
        elif dic['URI']:
            t = ("URI", dic['URI'], nlinha, m.span())
    
        elif dic['INT']:
            t = ("INT", dic['INT'], nlinha, m.span())
    
        elif dic['ABRE_CHAVES']:
            t = ("ABRE_CHAVES", dic['ABRE_CHAVES'], nlinha, m.span())
    
        elif dic['FECHA_CHAVES']:
            t = ("FECHA_CHAVES", dic['FECHA_CHAVES'], nlinha, m.span())
    
        elif dic['PONTO']:
            t = ("PONTO", dic['PONTO'], nlinha, m.span())
    
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], nlinha, m.span())
    
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], nlinha, m.span())
    
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], nlinha, m.span())
    
        else:
            t = ("UNKNOWN", m.group(), nlinha, m.span())
        if not dic['SKIP'] and t[0] != 'UNKNOWN': reconhecidos.append(t)
    return reconhecidos

nlinha = 1
for linha in sys.stdin:
    for tok in tokenize(linha):
        print(tok) 
    nlinha += 1   

