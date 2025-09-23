# TP1 - Especificação de uma expressão regular

## Autor
- Nome: Idy Saquina Carlos
- ID: A105237
- Foto:  
  ![Minha Foto](minhafoto.jpg)  

## Resumo
> Este trabalho consiste em especificar uma expressão regular que aceite **qualquer string binária que não contenha a substring `011`**.

## Expressão regular proposta:
#^(?:(?!011)[01])+$  

## Explicação:
- `^` — começa a analisar do início.
- `(?!.*011)` — garante que não existe a substring proibida.  
- `[01]*` — aceita qualquer combinação de 0s e 1s.  
- `$` — termina no fim da string, garantindo que toda a string respeita a regra. 


### Exemplos de teste

## Strings válidas (devem casar):
- `1111111`
- `000001`
- `1111010101000`

## Strings inválidas (não devem casar):
- `111010110111`
- `011`
- `00000001100000000`

## Lista de Resultados
- [regex.py](regex.py) — programa em Python que valida strings a partir do ficheiro `teste.txt`
- [teste.txt](teste.txt) — ficheiro com exemplos de strings válidas e inválidas
