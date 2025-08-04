import random

# Gerar uma lista com 250 números inteiros aleatórios entre 1 e 1000
numeros = [random.randint(1, 1000) for _ in range(250)]

# Reverter a lista
numeros.reverse()

# Imprimir o resultado
print(numeros)
