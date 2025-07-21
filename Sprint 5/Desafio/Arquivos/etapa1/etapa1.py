import os
import pandas as pd
import boto3
import botocore
import datetime

# Constantes de configuração
NOME_DO_BUCKET = "data-lake-rhamon-pires-pb"
CAMINHO_BASE = "Raw/Local/CSV"
PASTA_DADOS = "/data"

BATCH_SIZE = 100  # tamanho do batch para CSV filtrado

ARQUIVOS_PARA_ENVIAR = [
    ("movies.csv", "Movies"),
    ("series.csv", "Series"),
]

def criar_cliente_s3():
    return boto3.client('s3')

def criar_bucket(bucket_nome, cliente_s3):
    try:
        cliente_s3.head_bucket(Bucket=bucket_nome)
        print(f"Bucket '{bucket_nome}' já existe.")
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code in ['404', 'NoSuchBucket']:
            cliente_s3.create_bucket(Bucket=bucket_nome)
            print(f"Bucket '{bucket_nome}' criado com sucesso.")
        elif error_code in ['403', 'AccessDenied']:
            print(f"Você não tem permissão para acessar o bucket '{bucket_nome}'.")
        else:
            raise

def upload_csv(cliente_s3, pasta_nome, arquivo_nome, categoria):
    hoje = datetime.date.today()
    caminho_s3 = f"{CAMINHO_BASE}/{categoria}/{hoje.year}/{hoje.month:02d}/{hoje.day:02d}/{arquivo_nome}"

    try:
        cliente_s3.head_object(Bucket=NOME_DO_BUCKET, Key=caminho_s3)
        print(f"O arquivo '{caminho_s3}' já existe em '{NOME_DO_BUCKET}'. Upload ignorado.")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            caminho_local = os.path.join(pasta_nome, arquivo_nome)
            cliente_s3.upload_file(caminho_local, NOME_DO_BUCKET, caminho_s3)
            print(f"Arquivo '{arquivo_nome}' enviado para 's3://{NOME_DO_BUCKET}/{caminho_s3}'")
        else:
            raise

def gerar_csv_id_filtrados(pasta_nome, arquivo_leitura, arquivo_saida, batch_size=BATCH_SIZE):
    """
    Lê CSV de entrada em pasta_nome/arquivo_leitura,
    filtra os IDs,
    salva resultado em batches de batch_size em pasta_nome,
    nome dos arquivos: arquivo_saida_1.csv, arquivo_saida_2.csv, ...
    """
    import math

    caminho_entrada = os.path.join(pasta_nome, arquivo_leitura)

    df = pd.read_csv(caminho_entrada, sep='|')

    df_unico = df.drop_duplicates(subset=['id']).copy()
    df_filtrado_genero = df_unico[
        df_unico['genero'].str.contains('Romance', case=False, na=False) |
        df_unico['genero'].str.contains('Drama', case=False, na=False)
    ].copy()

    C = df_filtrado_genero['notaMedia'].mean()
    m = df_filtrado_genero['numeroVotos'].quantile(0.95)

    def weighted_rating(x, m=m, C=C):
        v = x['numeroVotos']
        R = x['notaMedia']
        return (v / (v + m) * R) + (m / (v + m) * C)

    df_filtrado_genero['weighted_rating'] = df_filtrado_genero.apply(weighted_rating, axis=1)
    df_filtrado = df_filtrado_genero[df_filtrado_genero['numeroVotos'] >= m]
    filmes_sucesso = df_filtrado[df_filtrado['weighted_rating'] > 7].sort_values(by='weighted_rating', ascending=False)

    print(f"{len(filmes_sucesso)} filmes filtrados para consulta na API")

    # Quebra em batches
    total = len(filmes_sucesso)
    n_batches = math.ceil(total / batch_size)

    for i in range(n_batches):
        inicio = i * batch_size
        fim = inicio + batch_size
        batch_df = filmes_sucesso.iloc[inicio:fim]

        nome_arquivo_batch = f"{arquivo_saida.replace('.csv','')}_{i+1}.csv"
        caminho_saida = os.path.join(pasta_nome, nome_arquivo_batch)

        batch_df[['id']].to_csv(caminho_saida, index=False)

        ARQUIVOS_PARA_ENVIAR.append((os.path.basename(caminho_saida), "Movies Filtrados ID"))

        print(f"Batch {i+1} salvo em {caminho_saida}")


if __name__ == "__main__":
    cliente_s3 = criar_cliente_s3()

    # Cria o bucket caso não exista
    criar_bucket(NOME_DO_BUCKET, cliente_s3)

    # Gera o CSV filtrado localmente (mesma pasta para entrada e saída)
    gerar_csv_id_filtrados(PASTA_DADOS, "movies.csv", "movies_filtrado_id.csv")

    # Envia os arquivos configurados
    for arquivo, categoria in ARQUIVOS_PARA_ENVIAR:
        upload_csv(cliente_s3, PASTA_DADOS, arquivo, categoria)
