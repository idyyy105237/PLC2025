# TP4 - Analisador Léxico e Sintático para Expressões Aritméticas

## Autor
- Nome: Idy Saquina Carlos  
- ID: A105237  
- Foto:  
  ![Minha Foto](minhafoto.jpg)  

## Resumo
Este trabalho consiste em criar um **analisador léxico e sintático** para expressões aritméticas simples, capazes de lidar com números inteiros, operações de soma, subtração, multiplicação, divisão e parênteses.  

O **analisador léxico** identifica os tokens (números, operadores e parênteses), enquanto o **analisador sintático recursivo descendente** verifica se a expressão respeita a sintaxe correta, seguindo a prioridade natural das operações:

1. **Parênteses** têm prioridade máxima.  
2. **Multiplicação e divisão** têm prioridade sobre soma e subtração.  
3. **Soma e subtração** têm prioridade mínima.  

A saída do analisador sintático indica se a expressão é válida ou não, permitindo construir posteriormente uma árvore sintática ou avaliar a expressão.

## A gramática utilizada segue esta hierarquia:
S         -> Literal MaisMenos
MaisMenos -> '+' Literal MaisMenos | '-' Literal MaisMenos | Eps
Literal   -> Fator MultDiv
MultDiv   -> '*' Fator MultDiv | '/' Fator MultDiv | Eps
Fator     -> Int | '(' S ')'

---

## Lista de Resultados
| Descrição                                   | Ficheiro                          |
| ------------------------------------------- | --------------------------------- |
| Analisador Léxico (tokenização)             | [`lexer_exp_arit.py`](./lexer_exp_arit.py) |
| Analisador Sintático Recursivo Descendente  | [`parser_exp_arit.py`](./parser_exp_arit.py) |

---


