import os
import pandas as pd
import re
import csv

csv_entrada = os.environ.get(
    "INPUT_CSV_ETL", "/etl/data/concert_tours_by_women.csv")
csv_saida = os.environ.get("OUTPUT_CSV", "/volume/csv_limpo.csv")

bad_lines = []
with open(csv_entrada, newline='', encoding='utf-8') as arquivo_csv:

    leitura = csv.reader(arquivo_csv)
    cabecalho = next(leitura)
    qtd_colunas = len(cabecalho)

    for i, linha in enumerate(leitura):
        if len(linha) != qtd_colunas:
            bad_lines.append(i)


df = pd.read_csv(csv_entrada)
df.drop(bad_lines, inplace=True)
df.drop_duplicates(inplace=True)


for i, linha in df.iterrows():

    referencias = set()
    linha_formatada = {}

    for col in df.columns:

        campo = str(linha[col])

        refs_encontradas = re.findall(r"\[[^\]]+\]", campo)
        referencias.update(refs_encontradas)

        campo = re.sub(r"\[[^\]]+\]", "", campo).strip()

        linha_formatada[col] = campo

    for col in df.columns:

        df[col] = df[col].astype(object)
        df.at[i, col] = str(linha_formatada[col])

    df.at[i, "Ref."] = ",".join(referencias)


df['Tour title'] = df['Tour title'].str.replace(
    r'[^\w\s]', '', regex=True).str.strip()


df[['Start Year', 'End Year']] = df['Year(s)'].str.split('-', expand=True)
df['End Year'] = df['End Year'].fillna(df['Start Year'])


cols = ['Rank', 'Peak', 'All Time Peak', 'Shows']

for col in cols:

    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

cols = ['Actual gross', 'Adjustedgross (in 2022 dollars)', 'Average gross']

for col in cols:

    df[col] = df[col].str.replace(r'[\$,]', '', regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')


df = df.rename(columns={
    'Adjustedgross (in 2022 dollars)': 'Adjusted gross (in 2022 dollars)'
})


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

df.to_csv(csv_saida, index=False)
