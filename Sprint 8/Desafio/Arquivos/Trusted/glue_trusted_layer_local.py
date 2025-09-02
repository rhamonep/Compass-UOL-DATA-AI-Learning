<<<<<<< HEAD
#!/usr/bin/env python3
"""
Script Spark para AWS Glue - Camada Trusted Local
Processa dados da camada Raw Local e cria a camada Trusted
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Inicialização do Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'CSV_RAW_PATH', 'TRUSTED_BASE_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def obter_caminhos_s3():
    """Obtém os caminhos S3 das camadas"""
    caminho_csv_raw = args['CSV_RAW_PATH']
    caminho_trusted_base = args['TRUSTED_BASE_PATH']
    
    caminho_trusted_local = f"{caminho_trusted_base}/Local/Parquet/Movies"
    
    return {
        'csv_raw': caminho_csv_raw,
        'trusted_local': caminho_trusted_local
    }

def ler_dados_csv():
    """Lê os dados CSV da camada Raw"""
    caminhos = obter_caminhos_s3()
    
    df_csv = spark.read.csv(
        caminhos['csv_raw'],
        header=True
    )
    
    return df_csv

def explodir_campos_csv(df_csv):
    """Explode campos multivalorados do CSV"""
    
    # Renomeia a coluna original para evitar conflito
    df_renomeado = df_csv.withColumnRenamed("genero", "generos")
    
    # Define as colunas base que serão mantidas
    campos_base = ['id', 'tituloPincipal', 'tempoMinutos', 'notaMedia', 'numeroVotos']
    
    # Explode o campo generos (separa por vírgula e cria uma linha para cada gênero)
    df_explodido = df_renomeado.select(
        campos_base + ['generos']
    ).select(
        '*',
        explode_outer(split(col('generos'), ',')).alias("genero")
    ).drop('generos')  # Remove a coluna generos original
    
    return df_explodido

def aplicar_tratamentos_qualidade(df):
    """Aplica tratamentos básicos de qualidade de dados"""
    
    colunas_string = [col for col in df.columns if df.schema[col].dataType == StringType()]
    for coluna in colunas_string:
        df = df.withColumn(coluna, trim(col(coluna)))
    
    return df

def processar_dados_trusted(df_csv_explodido):
    """Processa dados para a camada Trusted"""
    
    colunas_finais = ['id', 'tituloPincipal', 'tempoMinutos', 'notaMedia', 'numeroVotos', 'genero']
    
    df_csv_trusted = df_csv_explodido.select(colunas_finais)
    
    return df_csv_trusted

def salvar_camada_trusted(df_csv_trusted):
    """Salva os dados na camada Trusted"""
    caminhos = obter_caminhos_s3()

    df_csv_trusted = aplicar_tratamentos_qualidade(df_csv_trusted)

    hoje = datetime.now()
    ano = hoje.strftime('%Y')
    mes = hoje.strftime('%m')
    dia = hoje.strftime('%d')
    
    caminho_completo = f"{caminhos['trusted_local']}/{ano}/{mes}/{dia}"
    
    df_csv_trusted.write.mode("overwrite").parquet(caminho_completo)

def main():
    """Função principal do job Glue"""
    try:
        
        df_csv = ler_dados_csv()

        df_csv_explodido = explodir_campos_csv(df_csv)

        df_csv_trusted = processar_dados_trusted(df_csv_explodido)

        salvar_camada_trusted(df_csv_trusted)

    except Exception as e:
        raise
    finally:
        job.commit()

if __name__ == "__main__":
    main()
=======
#!/usr/bin/env python3
"""
Script Spark para AWS Glue - Camada Trusted Local
Processa dados da camada Raw Local e cria a camada Trusted
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime

# Inicialização do Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'CSV_RAW_PATH', 'TRUSTED_BASE_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def obter_caminhos_s3():
    """Obtém os caminhos S3 das camadas"""
    caminho_csv_raw = args['CSV_RAW_PATH']
    caminho_trusted_base = args['TRUSTED_BASE_PATH']
    
    caminho_trusted_local = f"{caminho_trusted_base}/Local/Parquet/Movies"
    
    return {
        'csv_raw': caminho_csv_raw,
        'trusted_local': caminho_trusted_local
    }

def ler_dados_csv():
    """Lê os dados CSV da camada Raw"""
    caminhos = obter_caminhos_s3()
    
    df_csv = spark.read.csv(
        caminhos['csv_raw'],
        header=True
    )
    
    return df_csv

def explodir_campos_csv(df_csv):
    """Explode campos multivalorados do CSV"""
    
    # Renomeia a coluna original para evitar conflito
    df_renomeado = df_csv.withColumnRenamed("genero", "generos")
    
    # Define as colunas base que serão mantidas
    campos_base = ['id', 'tituloPincipal', 'tempoMinutos', 'notaMedia', 'numeroVotos']
    
    # Explode o campo generos (separa por vírgula e cria uma linha para cada gênero)
    df_explodido = df_renomeado.select(
        campos_base + ['generos']
    ).select(
        '*',
        explode_outer(split(col('generos'), ',')).alias("genero")
    ).drop('generos')  # Remove a coluna generos original
    
    return df_explodido

def aplicar_tratamentos_qualidade(df):
    """Aplica tratamentos básicos de qualidade de dados"""
    
    colunas_string = [col for col in df.columns if df.schema[col].dataType == StringType()]
    for coluna in colunas_string:
        df = df.withColumn(coluna, trim(col(coluna)))
    
    return df

def processar_dados_trusted(df_csv_explodido):
    """Processa dados para a camada Trusted"""
    
    colunas_finais = ['id', 'tituloPincipal', 'tempoMinutos', 'notaMedia', 'numeroVotos', 'genero']
    
    df_csv_trusted = df_csv_explodido.select(colunas_finais)
    
    return df_csv_trusted

def salvar_camada_trusted(df_csv_trusted):
    """Salva os dados na camada Trusted"""
    caminhos = obter_caminhos_s3()

    df_csv_trusted = aplicar_tratamentos_qualidade(df_csv_trusted)

    hoje = datetime.now()
    ano = hoje.strftime('%Y')
    mes = hoje.strftime('%m')
    dia = hoje.strftime('%d')
    
    caminho_completo = f"{caminhos['trusted_local']}/{ano}/{mes}/{dia}"
    
    df_csv_trusted.write.mode("overwrite").parquet(caminho_completo)

def main():
    """Função principal do job Glue"""
    try:
        
        df_csv = ler_dados_csv()

        df_csv_explodido = explodir_campos_csv(df_csv)

        df_csv_trusted = processar_dados_trusted(df_csv_explodido)

        salvar_camada_trusted(df_csv_trusted)

    except Exception as e:
        raise
    finally:
        job.commit()

if __name__ == "__main__":
    main()
>>>>>>> 53748dd930b2c36edb9b3adbda3e293b1e4298e3
