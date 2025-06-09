'''
Exercícios Parte 3
Você está recebendo um arquivo contendo 10.000 números inteiros, um em cada linha. 
Utilizando lambdas e high order functions, apresente os 5 maiores valores pares e a soma destes.

Você deverá aplicar as seguintes funções no exercício:

- map
- filter
- sorted
- sum

Seu código deverá exibir na saída (simplesmente utilizando 2 comandos `print()`):

a lista dos 5 maiores números pares em ordem decrescente;

a soma destes valores.
'''

with open("number.txt", "r") as f:
    linhas = f.readlines()

numeros = list(map(lambda x: int(x.strip()), linhas))
pares = list(filter(lambda x: x % 2 == 0, numeros))
pares_ordenados = sorted(pares, reverse=True)
top5 = pares_ordenados[:5]
soma_top5 = sum(top5)

print(top5)
print(soma_top5)
