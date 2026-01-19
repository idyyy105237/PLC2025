# Compilador para Pascal Standard

Este projeto descreve o desenvolvimento de um compilador para a linguagem **Pascal Standard**, implementado em **Python** com a biblioteca **PLY (Python Lex-Yacc)**.

O compilador suporta um subconjunto representativo da linguagem, incluindo:  
- Declarações de variáveis e arrays  
- Expressões aritméticas, relacionais e lógicas  
- Estruturas de controlo (`if`, `while`, `for`)  
- Operações básicas de entrada e saída (`readln`, `writeln`)  

O processo de compilação inclui:  
1. **Análise léxica**: identificação de tokens a partir do código fonte  
2. **Análise sintática**: construção da **Árvore Sintática Abstrata (AST)**  
3. **Análise semântica**: validação de tipos, declaração prévia de variáveis e consistência de escopos, utilizando uma **tabela de símbolos**  
4. **Geração de código para máquina virtual**: tradução da AST em instruções executáveis, respeitando a semântica do programa  

O compilador é modular, permitindo testes e manutenção independentes de cada fase, e produz código que pode ser executado numa **máquina virtual fornecida**.
