# TP2 - Conversor de MarkDown para HTML

## Autor
- Nome: Idy Saquina Carlos
- ID: A105237
- Foto:  
  ![Minha Foto](minhafoto.jpg)  

## Resumo
Este trabalho consiste em criar um pequeno conversor de Markdown para HTML em Python, suportando os elementos básicos descritos na "Basic Syntax" da Cheat Sheet: cabeçalhos (#, ##, ###), texto em bold, itálico, listas numeradas, links e imagens.

## Funcionalidades implementadas
- Cabeçalhos: #, ##, ### → <h1>, <h2>, <h3>
- Texto em negrito: **texto** → <b>texto</b>  
- Texto em itálico: *texto* → <i>texto</i>  
- Listas numeradas: 1. item → <ol><li>item</li></ol>
- Links: [texto](url) → <a href="url">texto</a>
- Imagens: ![alt](src) → <img src="src" alt="alt"/>

## Explicação:
Cabeçalhos (#, ##, ###) → <h1>, <h2>, <h3>
Detectados com regex no início da linha; o número de # indica o nível do cabeçalho.

Negrito (**texto**) → <b>texto</b>
Regex detecta **...** e substitui por <b>...</b>; aplicado antes do itálico para evitar conflitos.

Itálico (*texto*) → <i>texto</i>
Regex detecta *...* e substitui por <i>...</i>; aplicado após o negrito.

Listas numeradas (1. item) → <ol><li>item</li></ol>
Linhas numeradas são acumuladas; ao terminar a sequência, envolvidas em <ol>...</ol>.

Links ([texto](url)) → <a href="url">texto</a>
Regex captura texto e URL; substitui por <a href="url">texto</a>.

Imagens (![alt](src)) → <img src="src" alt="alt"/>
Regex detecta ![alt](src); substituídas por <img src="src" alt="alt"/>; processadas antes dos links.


## Lista de Resultados
- [md2html](md2html) — programa em Python que conerte MarkDown para HTML a partir do ficheiro `mkd.md`
- [mkd.md](mkd.md) — ficheiro com exemplos do input
