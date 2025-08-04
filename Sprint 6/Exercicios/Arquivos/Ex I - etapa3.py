import random
import names  # Biblioteca para gerar nomes aleatórios

# Parâmetros para geração do dataset
qtd_nomes_aleatorios = 10_000_000     # Quantidade total de nomes gerados
qtd_nomes_unicos = 39_080          # Quantidade de nomes únicos desejados

# Definir a semente de aleatoriedade para resultados reproduzíveis
random.seed(40)

# Gerar nomes únicos
aux = []  # Lista para armazenar nomes únicos

for i in range(0, qtd_nomes_unicos):
    aux.append(names.get_full_name())  # Adicionar o nome à lista de nomes únicos

print(f'Gerando {qtd_nomes_aleatorios} nomes aleatórios')

# Gerar lista final com nomes aleatórios (podendo repetir), escolhendo entre os nomes únicos
dados = []
for i in range(qtd_nomes_aleatorios):
    dados.append(random.choice(aux))

# Salvar os nomes em um arquivo texto, um nome por linha
with open("nomes_aleatorios.txt", "w", encoding="utf-8") as arquivo:
    for nome in dados:
        arquivo.write(nome + "\n")

print("Arquivo 'nomes_aleatorios.txt' gerado com sucesso!")
