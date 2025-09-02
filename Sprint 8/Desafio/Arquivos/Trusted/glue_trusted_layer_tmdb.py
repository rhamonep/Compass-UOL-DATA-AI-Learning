#!/usr/bin/env python3

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

# Configurações de Performance do Spark
SPARK_CONFIGS = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.localShuffleReader.enabled": "true"
}

# Configurações de Processamento
PROCESSING_CONFIGS = {
    "particoes_iniciais": 20,
    "particoes_explodidas": 50
}

# Configurações dos Campos
FIELD_CONFIGS = {
    "campos_base": ['imdb_id', 'tmdb_revenue', 'tmdb_budget', 'tmdb_release_date', 'tmdb_popularity', 'tmdb_adult'],
    "campos_para_explodir": ['tmdb_genres', 'tmdb_keywords', 'tmdb_production_countries'],
    "campos_string": ['genres', 'keywords', 'production_countries']
}

# =============================================================================
# INICIALIZAÇÃO DO GLUE
# =============================================================================

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'JSON_RAW_PATH', 'TRUSTED_BASE_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Aplica configurações do Spark
for config, value in SPARK_CONFIGS.items():
    spark.conf.set(config, value)

def obter_caminhos_s3():
    """Obtém os caminhos S3 das camadas"""
    caminho_json_raw = args['JSON_RAW_PATH']
    caminho_trusted_base = args['TRUSTED_BASE_PATH']
    
    caminho_trusted_tmdb = f"{caminho_trusted_base}/TMDB/Parquet/Movies"
    
    return {
        'json_raw': caminho_json_raw,
        'trusted_tmdb': caminho_trusted_tmdb
    }

def ler_dados_json():
    """Lê os dados JSON da camada Raw"""
    caminhos = obter_caminhos_s3()
    
    # Lê JSON com configurações otimizadas
    df_json = spark.read.option("multiline", "true").json(caminhos['json_raw'])
    
    # Repartição otimizada usando configuração global
    df_json = df_json.repartition(PROCESSING_CONFIGS["particoes_iniciais"])
    
    # Cache dos dados para evitar releitura
    df_json.cache()
    
    return df_json

def explodir_campos_json(df_json):
    """Explode campos multivalorados do JSON"""
    
    # Usa configurações globais
    campos_base = FIELD_CONFIGS["campos_base"]
    campos_para_explodir = FIELD_CONFIGS["campos_para_explodir"]
    
    dfs_explodidos = []
    
    # Explode cada campo multivalorado separadamente
    for campo in campos_para_explodir:
        # Define o nome do campo de saída (remove tmdb_ e não adiciona _item)
        campo_saida = campo.replace('tmdb_', '')
        
        df_explodido = df_json.select(
            campos_base + [campo]
        ).select(
            '*',
            explode(split(col(campo), ', ')).alias(campo_saida)
        ).drop(campo)
        
        dfs_explodidos.append(df_explodido)
    
    # Combina todos os DataFrames
    df_final = dfs_explodidos[0]
    for df in dfs_explodidos[1:]:
        df_final = df_final.unionByName(df, allowMissingColumns=True)
    
    # Repartição otimizada usando configuração global
    df_final = df_final.repartition(PROCESSING_CONFIGS["particoes_explodidas"])
    
    return df_final

def aplicar_tratamentos_qualidade(df):
    """Aplica tratamentos básicos de qualidade de dados"""
    
    # Aplica trim em todas as colunas string usando configuração global
    for coluna in FIELD_CONFIGS["campos_string"]:
        df = df.withColumn(coluna, trim(col(coluna)))
    
    return df

def processar_dados_trusted(df_json_explodido):
    """Processa dados para a camada Trusted"""
    
    # Renomeia campos com prefixo tmdb_ para nomes finais
    df_renomeado = df_json_explodido \
        .withColumnRenamed('tmdb_revenue', 'revenue') \
        .withColumnRenamed('tmdb_budget', 'budget') \
        .withColumnRenamed('tmdb_release_date', 'release_date') \
        .withColumnRenamed('tmdb_popularity', 'popularity') \
        .withColumnRenamed('tmdb_adult', 'adult')
    
    # Define colunas finais
    colunas_finais = ['imdb_id', 'revenue', 'budget', 'release_date', 'popularity', 'adult'] + FIELD_CONFIGS["campos_string"]
    
    df_json_trusted = df_renomeado.select(colunas_finais)
    
    return df_json_trusted

def salvar_camada_trusted(df_json_trusted):
    """Salva os dados na camada Trusted"""
    caminhos = obter_caminhos_s3()

    df_json_trusted = aplicar_tratamentos_qualidade(df_json_trusted)

    hoje = datetime.now()
    ano = hoje.strftime('%Y')
    mes = hoje.strftime('%m')
    dia = hoje.strftime('%d')
    
    caminho_completo = f"{caminhos['trusted_tmdb']}/{ano}/{mes}/{dia}"
    
    # Salva dados Parquet deixando o Spark decidir o tamanho dos arquivos
    df_json_trusted.write \
        .mode("overwrite") \
        .option("compression", "snappy") \
        .parquet(caminho_completo)

def main():
    """Função principal do job Glue"""
    try:
        print("=== INICIANDO PROCESSAMENTO TMDB CAMADA TRUSTED ===")
        
        # Etapa 1: Leitura dos dados
        print("1. Lendo dados JSON...")
        df_json = ler_dados_json()
        
        # Etapa 2: Explosão de campos multivalorados
        print("2. Explodindo campos multivalorados...")
        df_json_explodido = explodir_campos_json(df_json)
        
        # Etapa 3: Processamento para camada trusted
        print("3. Processando dados trusted...")
        df_json_trusted = processar_dados_trusted(df_json_explodido)
        
        # Etapa 4: Salvamento
        print("4. Salvando dados...")
        salvar_camada_trusted(df_json_trusted)
        
        # Limpeza de recursos
        print("5. Limpando recursos...")
        df_json.unpersist()
        
        print("=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"ERRO durante o processamento: {e}")
        raise
    finally:
        job.commit()

if __name__ == "__main__":
    main()
