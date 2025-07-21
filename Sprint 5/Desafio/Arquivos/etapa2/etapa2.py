import os
import json
import logging
import time
import requests
from io import StringIO

import boto3
import pandas as pd
from tmdbv3api import TMDb, Movie

# Configurações fixas
S3_BUCKET = "data-lake-rhamon-pires-pb"
S3_PREFIX_CSV = "Raw/Local/CSV/Movies Filtrados ID/2025/07/21"
S3_PREFIX_JSON = "Raw/Local/JSON/2025/07/22"
BASE_DELAY = 0.25  # segundos

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# TMDb API
tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")
tmdb.language = "pt-BR"
movie_api = Movie()

# Sessão requests para usar nas chamadas customizadas e reaproveitar conexões
session = requests.Session()

s3 = boto3.client("s3")


def ler_csv_de_s3(bucket, key, delimiter='|'):

    logger.info(f"Lendo CSV do S3: s3://{bucket}/{key}")

    response = s3.get_object(Bucket=bucket, Key=key)

    with response['Body'] as stream:
        csv_string = stream.read().decode('utf-8')

    return pd.read_csv(StringIO(csv_string), delimiter=delimiter)


def salvar_no_s3(dados, caminho):

    json_bytes = json.dumps(dados, ensure_ascii=False).encode('utf-8')
    s3.put_object(Bucket=S3_BUCKET, Key=caminho, Body=json_bytes)
    logger.info(f"Arquivo salvo em s3://{S3_BUCKET}/{caminho}")

def extrair_dados_tmdb(tmdb_or_imdb_id):
    try:
        # Se o ID for do tipo IMDb (começa com 'tt'), resolve para o TMDb ID primeiro
        if tmdb_or_imdb_id.startswith("tt"):
            find_url = f"https://api.themoviedb.org/3/find/{tmdb_or_imdb_id}"
            params_find = {
                "api_key": tmdb.api_key,
                "external_source": "imdb_id"
            }
            resp_find = session.get(find_url, params=params_find)
            resp_find.raise_for_status()
            data_find = resp_find.json()
            movie_results = data_find.get("movie_results", [])
            if not movie_results:
                logger.warning(f"Nenhum resultado TMDb para IMDb ID {tmdb_or_imdb_id}")
                return None
            tmdb_id = movie_results[0]["id"]
        else:
            tmdb_id = tmdb_or_imdb_id  # já é um TMDb ID numérico

        # Agora faz a chamada oficial para /movie/{id} com append=credits
        base_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {
            "api_key": tmdb.api_key,
            "language": tmdb.language,
            "append_to_response": "credits"
        }
        response = session.get(base_url, params=params)
        response.raise_for_status()
        detalhes = response.json()

        creditos = detalhes.get("credits", {})
        elenco = creditos.get('cast', [])

        def contar_popularidade(itens):
            contagem = {"0_3": 0, "3_7": 0, "7_10": 0}
            for p in itens:
                pop = p.get("popularity") or 0
                if pop < 3:
                    contagem["0_3"] += 1
                elif pop < 7:
                    contagem["3_7"] += 1
                else:
                    contagem["7_10"] += 1
            return contagem

        elenco_pop = contar_popularidade(elenco)
        equipe_tec = creditos.get('crew', [])

        def filtrar_crew_por_job(job):
            return [c for c in equipe_tec if c.get("job") == job]

        diretores = filtrar_crew_por_job("Director")
        roteiristas = filtrar_crew_por_job("Writer")
        compositores = filtrar_crew_por_job("Original Music Composer")

        data = {
            "tmdb_id": detalhes.get("id"),
            "imdb_id": detalhes.get("imdb_id"),
            "titulo": detalhes.get("title"),
            "titulo_original": detalhes.get("original_title"),
            "ano_lancamento": detalhes.get("release_date", "")[:4] if detalhes.get("release_date") else None,
            "mes_lancamento": detalhes.get("release_date", "")[5:7] if detalhes.get("release_date") else None,
            "runtime": detalhes.get("runtime"),
            "budget": detalhes.get("budget"),
            "revenue": detalhes.get("revenue"),
            "popularity": detalhes.get("popularity"),
            "vote_average": detalhes.get("vote_average"),
            "vote_count": detalhes.get("vote_count"),
            "adult": detalhes.get("adult"),
            "generos": [g['name'] for g in detalhes.get("genres", [])],
            "prod_companies": [c['name'] for c in detalhes.get("production_companies", [])],
            "prod_countries": [c['name'] for c in detalhes.get("production_countries", [])],
            "cast_count": len(elenco),
            "cast_popularity_0_3": elenco_pop["0_3"],
            "cast_popularity_3_7": elenco_pop["3_7"],
            "cast_popularity_7_10": elenco_pop["7_10"],
            "directors_count": len(diretores),
            "directors_pop_0_3": contar_popularidade(diretores)["0_3"],
            "directors_pop_3_7": contar_popularidade(diretores)["3_7"],
            "directors_pop_7_10": contar_popularidade(diretores)["7_10"],
            "writers_count": len(roteiristas),
            "writers_pop_0_3": contar_popularidade(roteiristas)["0_3"],
            "writers_pop_3_7": contar_popularidade(roteiristas)["3_7"],
            "writers_pop_7_10": contar_popularidade(roteiristas)["7_10"],
            "composers_count": len(compositores),
            "composers_pop_0_3": contar_popularidade(compositores)["0_3"],
            "composers_pop_3_7": contar_popularidade(compositores)["3_7"],
            "composers_pop_7_10": contar_popularidade(compositores)["7_10"],
        }
        return data

    except Exception as e:
        logger.error(f"Erro ao extrair dados TMDb {tmdb_or_imdb_id}: {e}")
        return None



def lambda_handler(event, context):
    logger.info(f"Evento recebido: {event}")

    if isinstance(event, str):
        event = json.loads(event)

    # Se o evento vier com "body" (exemplo API Gateway), tenta extrair o json
    if "body" in event:

        try:
            event = json.loads(event["body"])
            logger.info(f"Evento extraído do body: {event}")
        except Exception as e:
            logger.error(f"Falha ao desserializar body: {e}")

    csv_key = event.get("csv_s3_key")

    if not csv_key:
        logger.error("Nenhum csv_s3_key informado no payload.")
        return {
            "statusCode": 400,
            "body": "Erro: parâmetro 'csv_s3_key' obrigatório."
        }

    logger.info(f"Processando arquivo CSV: s3://{S3_BUCKET}/{csv_key}")

    try:
        df = ler_csv_de_s3(S3_BUCKET, csv_key)

    except Exception as e:
        logger.error(f"Erro ao ler {csv_key}: {e}")
        return {
            "statusCode": 500,
            "body": f"Erro ao ler arquivo CSV: {e}"
        }

    lista_ids = df["id"].astype(str).str.strip().tolist()
    resultados = []

    for tmdb_id in lista_ids:
        try:
            dados = extrair_dados_tmdb(tmdb_id)
            resultados.append(dados)
            time.sleep(BASE_DELAY)

        except Exception as e:
            logger.warning(f"Erro ao extrair dados TMDb ID {tmdb_id}: {e}")
            continue

    if resultados:

        try:

            base_name = os.path.basename(csv_key).rsplit('.', 1)[0] + ".json"
            json_key = f"{S3_PREFIX_JSON}/{base_name}"

            salvar_no_s3(resultados, json_key)

        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
            return {
                "statusCode": 500,
                "body": f"Erro ao salvar resultados: {e}"
            }

    logger.info(f"Arquivo processado com sucesso: {csv_key}")
    return {
        "statusCode": 200,
        "body": f"Arquivo processado: {csv_key}"
    }
