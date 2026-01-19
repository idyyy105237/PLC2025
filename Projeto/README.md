# Compilador para Pascal Standard – Síntese do Projeto

O projeto consistiu na implementação de um compilador para a linguagem **Pascal Standard**, desenvolvido em **Python** utilizando a biblioteca **PLY (Python Lex-Yacc)** para análise léxica e sintática.

O compilador segue a estrutura clássica:

- **Análise Léxica (Lexer)**:  
  Converte o código-fonte em tokens, identificando palavras reservadas, operadores, identificadores, constantes e delimitadores, e detectando erros léxicos.

- **Análise Sintática (Parser)**:  
  Verifica se a sequência de tokens obedece à gramática da linguagem, construindo a **Árvore Sintática Abstrata (AST)**. Os blocos e comandos (atribuições, ciclos, condicionais) são processados nesta fase.

- **Análise Semântica**:  
  Valida a correção semântica do programa, garantindo compatibilidade de tipos, declaração prévia de variáveis e consistência de escopos. Erros semânticos são reportados com linha e contexto. A tabela de símbolos é construída com informações sobre variáveis, arrays (`lower`, `upper`, tamanho) e **offsets** para alocação de memória.

- **Geração de Código para Máquina Virtual (MV)**:  
  A AST é percorrida recursivamente, produzindo instruções de baixo nível que preservam a semântica do programa. Estruturas de controlo, expressões e operações de entrada/saída são traduzidas em instruções, utilizando offsets e etiquetas para gerir memória e fluxo de execução.

O compilador é **modular**, permitindo testes e manutenção independentes de cada fase. A execução final ocorre numa **máquina virtual fornecida**, garantindo que programas válidos são corretamente processados.
