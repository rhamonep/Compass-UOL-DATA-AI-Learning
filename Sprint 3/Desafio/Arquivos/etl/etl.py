import os
import pandas as pd
import re
import csv

# Caminhos dos arquivos extraídos do .env (csv de entrada e csv de saída)
csv_entrada = os.environ.get(
    "INPUT_CSV_ETL", "/etl/data/concert_tours_by_women.csv")
csv_saida = os.environ.get("OUTPUT_CSV", "/volume/csv_limpo.csv")

# Verificação de registros quebrados antes de abrir o dataframe com o pandas:
# Abre o csv e procura linhas que há uma quantidade de colunas diferentes do cabeçalho.

bad_lines = []
with open(csv_entrada, newline='', encoding='utf-8') as arquivo_csv:

    leitura = csv.reader(arquivo_csv)
    cabecalho = next(leitura)
    qtd_colunas = len(cabecalho)

    for i, linha in enumerate(leitura):
        if len(linha) != qtd_colunas:
            bad_lines.append(i)

# Abertura do csv como dataframe
df = pd.read_csv(csv_entrada)

# Remoção dos registros quebrados encontrados anteriormente e também dos duplicados
df.drop(bad_lines, inplace=True)
df.drop_duplicates(inplace=True)

# Busca e extração de referencias em campos errados. Substring no formato "[xx]"
for i, linha in df.iterrows():

    # Cria um conjunto vazio para armazenar as referencias, ja que não faz sentido referencias duplicadas.
    referencias = set()
    # inicia uma nova linha vazia que será a linha sem as substrings de referencia
    linha_formatada = {}

    for col in df.columns:

        campo = str(linha[col])  # acessa cada um dos campos da linha

        # usa regex para encontrar as substrings
        refs_encontradas = re.findall(r"\[[^\]]+\]", campo)
        # adiciona as referencias encontradas no conjunto para adicionar no campo correto.
        referencias.update(refs_encontradas)

        # apaga as referencias encontradas no campo atual
        campo = re.sub(r"\[[^\]]+\]", "", campo).strip()

        linha_formatada[col] = campo  # adiciona o campo limpo na nova linha.

    for col in df.columns:

        # tratar todas as colunas como object para evitar erros de conversão de tipos.
        df[col] = df[col].astype(object)
        # substitui a linha do dataframe equivalente pelo indice pela linha limpa (de coluna em coluna).
        df.at[i, col] = str(linha_formatada[col])

    # adiciona na coluna de referencias todas as referencias encontradas naquela linha.
    df.at[i, "Ref."] = ",".join(referencias)


# Busca e eliminação de caracteres que não sejam numeros e letras na coluna 'Tour title'"
df['Tour title'] = df['Tour title'].str.replace(
    r'[^\w\s]', '', regex=True).str.strip()

# Criação das colunas 'Start Year' e 'End Year' a partir da coluna 'Year(s)', extraindo cada ano separadamente a partir do caractere '-'."

df[['Start Year', 'End Year']] = df['Year(s)'].str.split('-', expand=True)
# Se não houver o caractere '-', o 'End Year' estara como NAN. Substitiur NAN pelo valor de ['Start Year']
df['End Year'] = df['End Year'].fillna(df['Start Year'])


# Formatação dos dados para os tipos corretos
# Colunas que possouem valor inteiro
cols = ['Rank', 'Peak', 'All Time Peak', 'Shows']

for col in cols:

    # converte a string do campo para INT, e em caso de falha atribuir NAN.
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

# Colunas que possouem valor float
cols = ['Actual gross', 'Adjustedgross (in 2022 dollars)', 'Average gross']

for col in cols:

    # Regex para encontrar os simbolo '$' e ',' e substitituir por vazio (apagar) antes de converter para FLOAT
    df[col] = df[col].str.replace(r'[\$,]', '', regex=True)
    # converte a string do campo para FLOAT, e em caso de falha atribuir NAN.
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')


# Renomeação da coluna 'Adjustedgross (in 2022 dollars)' para 'Adjusted gross (in 2022 dollars)' (adição do espaço)

df = df.rename(columns={
    'Adjustedgross (in 2022 dollars)': 'Adjusted gross (in 2022 dollars)'
})

# Manter apenas as colunas do dataframe conforme a especificação dada.

df = df[[
    'Rank',
    'Actual gross',
    'Adjusted gross (in 2022 dollars)',
    'Artist',
    'Tour title',
    'Shows',
    'Average gross',
    'Start Year',
    'End Year'
]]

# Exportar o dataframe para csv.
df.to_csv(csv_saida, index=False)
