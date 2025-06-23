import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

csv_entrada = os.environ.get("INPUT_CSV_JOB", "/volume/csv_limpo.csv")
respostas_txt = os.environ.get("OUTPUT_TXT", "/volume/respostas.txt")
grafico_q4_png = os.environ.get("GRAFICO_Q4", "/volume/Q4.png")
grafico_q5_png = os.environ.get("GRAFICO_Q5", "/volume/Q5.png")


df = pd.read_csv(csv_entrada)


def escrever_resposta(texto, arquivo=respostas_txt):

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        respostas = re.findall(r"Q\d+:", conteudo)
        proxima_qt = len(respostas) + 1

    except FileNotFoundError:
        proxima_qt = 1

    resposta_formatada = f"\nQ{proxima_qt}:\n--- {texto}\n"

    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(resposta_formatada)


with open(respostas_txt, "w", encoding="utf-8") as f:
    pass


contagem_turnes = df['Artist'].value_counts()
max_turnes = contagem_turnes.max()

artistas_mais_frequentes = contagem_turnes[contagem_turnes == max_turnes].index.tolist(
)

df_filtrado = df[df['Artist'].isin(artistas_mais_frequentes)]

medias_faturamento_artistas = df_filtrado.groupby('Artist')[
    'Actual gross'].mean()

artista_maior = medias_faturamento_artistas.idxmax()
media_maior = medias_faturamento_artistas.max()

escrever_resposta(
    f"\"{artista_maior}\" foi o artista que mais apareceu e teve a maior média de seu faturamento bruto, alcançando ${media_maior:,.2f}")


turnes_ano_unico = df[df['Start Year'] == df['End Year']]
turne_top = turnes_ano_unico.loc[turnes_ano_unico['Average gross'].idxmax()]


escrever_resposta(
    f"Entre as turnês realizadas em um ano, a \"{turne_top['Tour title']}\" teve a maior média de faturamento bruto, com ${turne_top['Average gross']:,.2f}")


df['Adjusted gross per show'] = df['Adjusted gross (in 2022 dollars)'] / \
    df['Shows']
top3 = df.nlargest(3, 'Adjusted gross per show')

output = "As 3 turnês com os shows unitários mais lucrativos foram:\n\n"

for count, (_, row) in enumerate(top3.iterrows(), 1):

    tour = row['Tour title']
    artist = row['Artist']
    gross_per_show = row['Adjusted gross per show']

    output += (f"{count}. \"{tour}\", do artista \"{artist}\", teve um faturamento médio de ${gross_per_show:,.2f} por show.\n")

escrever_resposta(output)


contagem_turnes = df['Artist'].value_counts()
max_turnes = contagem_turnes.max()

artistas_mais_frequentes = contagem_turnes[contagem_turnes == max_turnes].index.tolist(
)

df_filtrado = df[df['Artist'].isin(artistas_mais_frequentes)]

somatorio_faturamento_artistas = df_filtrado.groupby("Artist")[
    "Actual gross"].sum()

artista_maior = somatorio_faturamento_artistas.idxmax()

artist_df = df[df['Artist'] == artista_maior]

faturamento_ano = artist_df.groupby(
    "Start Year")["Actual gross"].sum().sort_index()

# Criar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(faturamento_ano.index, faturamento_ano.to_numpy(),
         marker='o', linestyle='-')

# Título e eixos
plt.title(f'{artista_maior} - Faturamento Bruto das turnês')
plt.xlabel('Ano',  fontsize=14, labelpad=15)
plt.ylabel('Faturamento Bruto (USD)',  fontsize=14, labelpad=15)

# Mostrar apenas anos com turnê no eixo X
plt.xticks(faturamento_ano.index)

# Formatador do eixo Y
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Adicionar valores abaixo e à direita dos pontos
for x, y in zip(faturamento_ano.index, faturamento_ano.values):
    plt.text(x + 0.1, y - 5e6, f'${y:,.0f}', ha='left', va='top', fontsize=9)

# Exibição final
plt.grid(True)
plt.tight_layout()

plt.savefig(grafico_q4_png, dpi=300, bbox_inches='tight')

# %%
shows_by_artist = df.groupby('Artist')['Shows'].sum()
top5_shows = shows_by_artist.sort_values(ascending=False).head(5)

cores = ['#e78ac3', '#66c2a5', '#fc8d62', '#8da0cb', '#c0d854']

plt.figure(figsize=(10, 6))

# Grid no fundo (zorder baixo)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

# Barras na frente (zorder alto)
barras = plt.bar(top5_shows.index, top5_shows.to_numpy(),
                 color=cores, zorder=5)

plt.title('Top 5 artistas com mais shows')
plt.xlabel('Artista', fontsize=14, labelpad=15)
plt.ylabel('Total de Shows', fontsize=14, labelpad=15)

# Adiciona valores nas barras
for barra in barras:
    height = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, height + 2, f'{int(height)}',
             ha='center', va='bottom', fontsize=11, zorder=10)

# Legenda fora do gráfico, mais pra cima na lateral direita
plt.legend(barras, top5_shows.index,
           loc='center left', bbox_to_anchor=(1, 0.9))

plt.tight_layout()

plt.savefig(grafico_q5_png, dpi=300, bbox_inches='tight')
