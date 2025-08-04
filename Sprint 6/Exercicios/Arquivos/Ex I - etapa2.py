# Lista com 20 nomes de animais
animais = [
    "gato", "cachorro", "elefante", "leão", "tigre",
    "urso", "coelho", "girafa", "zebra", "macaco",
    "cavalo", "panda", "rinoceronte", "hipopótamo", "lobo",
    "raposa", "jacaré", "coruja", "pinguim", "tartaruga"
]

# Ordenar a lista em ordem crescente
animais.sort()

# Iterar e imprimir um a um (usando list comprehension para imprimir)
[print(animal) for animal in animais]

# Salvar em arquivo texto, um animal por linha
with open("animais.txt", "w", encoding="utf-8") as arquivo:
    for animal in animais:
        arquivo.write(animal + "\n")
