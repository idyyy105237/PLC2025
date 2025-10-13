# TP4 - Analisador Léxico para a linguagem SPARQL

## Autor
- Nome: Idy Saquina Carlos
- ID: A105237
- Foto:  
  ![Minha Foto](minhafoto.jpg)  

## Resumo
Este trabalho consiste em criar um analisador léxico (lexer) para a linguagem SPARQL, responsável por identificar e classificar tokens em consultas SPARQL.
O objetivo é reconhecer elementos como palavras-chave (SELECT, WHERE, LIMIT), variáveis (?x), URIs (dbo:, foaf:), literais, comentários e símbolos estruturais ({, }, .).

O lexer lê o conteúdo de um ficheiro de consulta SPARQL e gera como saída uma lista de tokens identificados, juntamente com a sua posição e tipo.


## Lista de Resultados
| Descrição                                           | Ficheiro                                     |
| --------------------------------------------------- | -------------------------------------------- |
| Definição dos tokens e geração do analisador léxico | [`gen_tokenizer2.py`](./gen_tokenizer2.py)   |
| Ficheiro JSON com a definição dos tokens SPARQL     | [`tokens_SPARQL.json`](./tokens_SPARQL.json) |
| Lexer gerado automaticamente                        | [`analex_SPARQL.py`](./analex_SPARQL.py)     |
| Ficheiro de teste da query SPARQL                   | [`query_SPARQL.txt`](./query_SPARQL.txt)     |


## Execução
$ python gen_tokenizer2.py tokens_SPARQL.json | Out-File -Encoding utf8 analex_SPARQL.py
$ Get-Content query_SPARQL.txt | python analex_SPARQL.py
