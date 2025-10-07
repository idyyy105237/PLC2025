# TP2 - Conversor de MarkDown para HTML

## Autor
- Nome: Idy Saquina Carlos
- ID: A105237
- Foto:  
  ![Minha Foto](minhafoto.jpg)  

## Resumo
Este trabalho consiste em criar um pequeno conversor de Markdown para HTML em Python, suportando os elementos básicos descritos na "Basic Syntax" da Cheat Sheet: cabeçalhos (#, ##, ###), texto em bold, itálico, listas numeradas, links e imagens.

## Funcionalidades implementadas
O programa lê o Markdown linha a linha.

Classifica cada linha (cabeçalho, lista, texto normal).

Processa elementos inline na ordem: imagem → link → negrito → itálico.

Garante que listas são abertas e fechadas corretamente.


## Lista de Resultados
- [md2html](md2html) — programa em Python que conerte MarkDown para HTML a partir do ficheiro `mkd.md`
- [mkd.md](mkd.md) — ficheiro com exemplos do input
