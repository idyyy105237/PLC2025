"""
md2html.py - conversor simples Markdown -> HTML 
"""

import re
import sys

# regexes inline
RE_IMG   = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')         # ![alt](src)
RE_LINK  = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')         # [text](url)
RE_BOLD  = re.compile(r'\*\*(.+?)\*\*')                   # **bold**
RE_ITAL  = re.compile(r'\*(.+?)\*')                       # *italic*

# regexes de linha
RE_HEADER = re.compile(r'^(#{1,3})\s*(.*)$')              # #, ##, ###
RE_OLINE  = re.compile(r'^\s*(\d+)\.\s+(.*)$')            # 1. texto

def inline_replace(text):
    """Aplica substituições inline por ordem: imagem, link, bold, italic."""
    # Imagem antes do link porque sintaxe começa com !
    text = RE_IMG.sub(r'<img src="\2" alt="\1"/>', text)
    text = RE_LINK.sub(r'<a href="\2">\1</a>', text)
    # Bold antes do italic para evitar conflito com * dentro de **
    text = RE_BOLD.sub(r'<b>\1</b>', text)
    text = RE_ITAL.sub(r'<i>\1</i>', text)
    return text

def md_to_html(lines):
    """Converte uma sequência de linhas Markdown para HTML (lista de strings -> string)."""
    out = []
    in_ol = False
    ol_items = []

    for raw in lines:
        # remove \n mas preserva linha vazia
        line = raw.rstrip('\n')

        # cabeçalhos
        m = RE_HEADER.match(line)
        if m:
            # fechar lista numerada aberta
            if in_ol:
                out.append('<ol>')
                out.extend(f'<li>{inline_replace(item)}</li>' for item in ol_items)
                out.append('</ol>')
                ol_items = []
                in_ol = False

            level = len(m.group(1))
            text = m.group(2).strip()
            text = inline_replace(text)
            out.append(f'<h{level}>{text}</h{level}>')
            continue

        # linha de lista numerada
        m = RE_OLINE.match(line)
        if m:
            item_text = m.group(2).strip()
            # iniciar lista se necessário
            if not in_ol:
                in_ol = True
                ol_items = []
            ol_items.append(item_text)
            continue

        # linha vazia -> finaliza listas se necessário e adiciona linha vazia (ou ignora)
        if line.strip() == '':
            if in_ol:
                out.append('<ol>')
                out.extend(f'<li>{inline_replace(item)}</li>' for item in ol_items)
                out.append('</ol>')
                ol_items = []
                in_ol = False
            continue

        # linha normal de texto
        if in_ol:
            # se tivermos uma lista aberta e aparecer uma linha normal, fechamos a lista antes
            out.append('<ol>')
            out.extend(f'<li>{inline_replace(item)}</li>' for item in ol_items)
            out.append('</ol>')
            ol_items = []
            in_ol = False

        # processa inline e adiciona como parágrafo simples (texto em linha)
        out.append(inline_replace(line))

    # depois do loop, fechar lista se ficou aberta
    if in_ol:
        out.append('<ol>')
        out.extend(f'<li>{inline_replace(item)}</li>' for item in ol_items)
        out.append('</ol>')

    # junta com novas linhas (formatado)
    return '\n'.join(out)

def main():
    # ler a partir de ficheiro (argumento) ou stdin
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        with open(fname, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    html = md_to_html(lines)
    print(html)

if __name__ == '__main__':
    main()
