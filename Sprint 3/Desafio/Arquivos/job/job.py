import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

# Caminhos dos arquivos extraídos do .env (csv de entrada e txt e png de saída)
csv_entrada = os.environ.get("INPUT_CSV_JOB", "/volume/csv_limpo.csv")
respostas_txt = os.environ.get("OUTPUT_TXT", "/volume/respostas.txt")
grafico_q4_png = os.environ.get("GRAFICO_Q4", "/volume/Q4.png")
grafico_q5_png = os.environ.get("GRAFICO_Q5", "/volume/Q5.png")

# leitura do csv limpo como dataframe
df = pd.read_csv(csv_entrada)

# função que recebe o texto a ser escrito no txt e o coloca no formato de acordo com a especificação


def escrever_resposta(texto, arquivo=respostas_txt):

    try:
        # tenta abrir o arquivo como LEITURA (se ele existir)
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # usa regex para contar quantas vezes apareceram a substring "QX" afim de determinar o numero da proxima questao
        respostas = re.findall(r"Q\d+:", conteudo)
        # Calcula o numero da proxima questao baseado na quantidade de elementos encontrados anteriormente
        proxima_qt = len(respostas) + 1

    except FileNotFoundError:
        proxima_qt = 1  # no caso de não encontrar o arquivo, definir a proxima questão como sendo a Q1

    # Formatação especificada para cada resposta
    resposta_formatada = f"\nQ{proxima_qt}:\n--- {texto}\n"

    with open(arquivo, "a", encoding="utf-8") as f:  # Abrir o arquivo para escrita
        f.write(resposta_formatada)


# Criação do arquivo respostas.txt
# Cria ou substitui o arquivo existente por um em branco. Isso porque em cada execução desejamos que o arquivos seja escrito do zero.
with open(respostas_txt, "w", encoding="utf-8") as f:
    pass  # necessário execução de ao menos uma instrução apos "with".


# Ql - Qual é a artista que mais aparece nessa lista e possui a maior média de seu faturamento bruto (Actual gross)?

# Contagem de quantas turnes fizeram cada artista
contagem_turnes = df['Artist'].value_counts()
max_turnes = contagem_turnes.max()  # Extrai o maior numero de turnes

artistas_mais_frequentes = contagem_turnes[contagem_turnes == max_turnes].index.tolist(  # Busca cada artista que possui a contagem de turnes equivalentes ao maximo.
)

# Filtra o dataframe para apenas os registros que possuem aquele artista com o valor maximo de turnes
df_filtrado = df[df['Artist'].isin(artistas_mais_frequentes)]

medias_faturamento_artistas = df_filtrado.groupby('Artist')[  # Por cada artista, calcula a sua média de faturamentos brutos para verificar qual o maior.
    'Actual gross'].mean()

# Extrai apenas o nome do artista que possui a maior media de faturamentos brutos
artista_maior = medias_faturamento_artistas.idxmax()
# o valor da sua media de faturamentos brutos
media_maior = medias_faturamento_artistas.max()

# invoca a função para escrever no arquivo de saída
escrever_resposta(
    f"\"{artista_maior}\" foi o artista que mais apareceu e teve a maior média de seu faturamento bruto, alcançando ${media_maior:,.2f}")


# 02 - Das turnês que aconteceram dentro de um ano, qual a turnê com a maior média de faturamento bruto (Average gross)?

# filtra as turnes que duraram um ano. (ano de começo e ano de fim iguais)
turnes_ano_unico = df[df['Start Year'] == df['End Year']]
# usa funcão para encontrar a partir do indice o maior 'Average gross'.
turne_top = turnes_ano_unico.loc[turnes_ano_unico['Average gross'].idxmax()]

# invoca a função para escrever no arquivo de saída
escrever_resposta(
    f"Entre as turnês realizadas em um ano, a \"{turne_top['Tour title']}\" teve a maior média de faturamento bruto, com ${turne_top['Average gross']:,.2f}")


# Q3 - Quais são as 3 turnês que possuem o show (unitário) mais lucrativo? Cite também o nome de cada artista e
# o valor por show. Utilize a coluna "Adjusted gross (in 2022 dollars)". Caso necessário, crie uma coluna nova para
# essa conta.


df['Adjusted gross per show'] = df['Adjusted gross (in 2022 dollars)'] / \
    df['Shows']  # Para calcular e armazenar o lucro médio de cada show, adicionamos a coluna 'Adjusted gross per show'
# Sendo calculado como 'Adjusted gross (in 2022 dollars)' (como especificado) divido pela quantidade de shows.

# filtramos o df para os 3 registros com maiores valores para a coluna 'Adjusted gross per show'
top3 = df.nlargest(3, 'Adjusted gross per show')

# Criação da variavel para armazenar a string de resposta
output = "As 3 turnês com os shows unitários mais lucrativos foram:\n\n"

# Escreve os campos necessários para a resposta adicionar na string de resposta
for count, (_, row) in enumerate(top3.iterrows(), 1):

    tour = row['Tour title']
    artist = row['Artist']
    gross_per_show = row['Adjusted gross per show']

    # concatena as string para serem escritas
    output += (f"{count}. \"{tour}\", do artista \"{artist}\", teve um faturamento médio de ${gross_per_show:,.2f} por show.\n")

# invoca a função para escrever no arquivo de saída
escrever_resposta(output)


# Q4 - Para a artista que mais aparece nessa lista e que tenha 0 maior somatório de faturamento bruto, crie um
# gráfico de linhas que mostra 0 faturamento por ano da turnê (use a coluna Start Year). Apenas os anos com
# turnês.


# Contagem de quantas turnes fizeram cada artista
contagem_turnes = df['Artist'].value_counts()
max_turnes = contagem_turnes.max()  # Extrai o maior numero de turnes

artistas_mais_frequentes = contagem_turnes[contagem_turnes == max_turnes].index.tolist(  # Busca cada artista que possui a contagem de turnes equivalentes ao maximo.
)

# Filtra o dataframe para apenas os registros que possuem aquele artista com o valor maximo de turnes
df_filtrado = df[df['Artist'].isin(artistas_mais_frequentes)]

somatorio_faturamento_artistas = df_filtrado.groupby("Artist")[  # Por cada artista, calcula o somatório de faturamentos brutos para verificar qual o maior.
    "Actual gross"].sum()

# Extrai apenas o nome do artista que possui a maior media de faturamentos brutos
artista_maior = somatorio_faturamento_artistas.idxmax()

# filtra o dataframe para apenas os registros que possuem aquele artista
artist_df = df[df['Artist'] == artista_maior]

faturamento_ano = artist_df.groupby(  # Agrupa por faturamente anual, somando os faturamentos.
    "Start Year")["Actual gross"].sum().sort_index()


# Criação do gráfico de linha

plt.figure(figsize=(10, 6))
plt.plot(faturamento_ano.index, faturamento_ano.to_numpy(),   # passagem de parametros dos dados para criação do gráfico
         marker='o', linestyle='-')

plt.title(f'{artista_maior} - Faturamento Bruto das turnês')       # Título
# Eixo x: Tamanhos e margens
plt.xlabel('Ano',  fontsize=14, labelpad=15)
plt.ylabel('Faturamento Bruto (USD)',  fontsize=14,
           labelpad=15)   # Eixo y: Tamanhos e margens

plt.xticks(faturamento_ano.index)  # Mostrar apenas anos com turnê no eixo X


plt.gca().yaxis.set_major_formatter(        # Formatador do eixo Y para os valores aparecem como $xxx,xxx,xxx.xx
    ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Posicionamento dos valores no gráfico, abaixo e a direita dos pontos.
for x, y in zip(faturamento_ano.index, faturamento_ano.values):
    plt.text(x + 0.1, y - 5e6, f'${y:,.0f}', ha='left', va='top', fontsize=9)

plt.grid(True)  # exbir malha
plt.tight_layout()  # formato de layout


# Exportação do gráfico como PNG e definição de sua resolução.
plt.savefig(grafico_q4_png, dpi=300, bbox_inches='tight')


# Q5 - Faça um gráfico de colunas demonstrando as 5 artistas com mais shows na lista.


# Criação do gráfico de barras
# Agrupa por artista e soma as quantidade de shows. Mantem apenas os 5 maiores
top5_shows = df.groupby('Artist')['Shows'].sum().nlargest(5)

cores = ['#e78ac3', '#66c2a5', '#fc8d62', '#8da0cb',
         '#c0d854']  # Definição de cores para cada barra

plt.figure(figsize=(10, 6))

plt.grid(axis='y', linestyle='--', alpha=0.7,
         zorder=0)  # Grid por tras do grafico

barras = plt.bar(top5_shows.index, top5_shows.to_numpy(),   # passagem de parametros dos dados para criação do gráfico
                 color=cores, zorder=5)                 # Barras na frente

plt.title('Top 5 artistas com mais shows')      # Título
# Eixo x: Tamanhos e margens
plt.xlabel('Artista', fontsize=14, labelpad=15)
# Eixo y: Tamanhos e margens
plt.ylabel('Total de Shows', fontsize=14, labelpad=15)

for barra in barras:                   # Adiciona valores nas barras
    height = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, height + 2, f'{int(height)}',  # Posicionamento do valor acima e no meio da barra
             # tamanho do numero e prioridade de exibição
             ha='center', va='bottom', fontsize=11, zorder=10)

plt.legend(barras, top5_shows.index,               # Legenda fora do gráfico, na lateral direita a cima
           loc='center left', bbox_to_anchor=(1, 0.9))

plt.tight_layout()  # formato de layout

# Exportação do gráfico como PNG e definição de sua resolução.
plt.savefig(grafico_q5_png, dpi=300, bbox_inches='tight')
