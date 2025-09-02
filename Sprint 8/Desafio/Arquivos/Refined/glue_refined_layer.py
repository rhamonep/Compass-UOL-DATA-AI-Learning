<<<<<<< HEAD
#!/usr/bin/env python3
"""
Job AWS Glue para processamento da camada Refined
Processa dados da camada Trusted e cria modelagem dimensional
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
from datetime import datetime

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

# Configurações do Spark
SPARK_CONFIGS = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.localShuffleReader.enabled": "true",
    "spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold": "0",
    "spark.sql.adaptive.forceApply": "true",
    "spark.sql.adaptive.logLevel": "WARN"
}

# Configurações de processamento
PROCESSING_CONFIGS = {
    "particoes_iniciais": 10,
    "particoes_finais": 15,
    "limite_keyword_percentual": 0.01,
    "compression": "snappy"
}

# Colunas para reorganização
COLUNAS_TMDB = [
    'id_imdb', 'receita', 'orcamento', 'data_lancamento', 
    'popularidade_tmdb', 'genero', 'conteudo_adulto', 'pais_producao', 'keyword'
]

COLUNAS_LOCAL = [
    'id_imdb', 'titulo_principal', 'genero', 
    'duracao_minutos', 'nota_media', 'numero_votos'
]

# Schemas explícitos para garantir tipos consistentes
SCHEMA_DIM_FILME = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_imdb", StringType(), False),
    StructField("titulo_principal", StringType(), True)
])

SCHEMA_DIM_GENERO = StructType([
    StructField("id_genero", IntegerType(), False),
    StructField("genero", StringType(), False)
])

SCHEMA_DIM_KEYWORD = StructType([
    StructField("id_keyword", IntegerType(), False),
    StructField("keyword", StringType(), False)
])

SCHEMA_DIM_TEMPO = StructType([
    StructField("id_tempo", IntegerType(), False),
    StructField("data_lancamento", DateType(), False),
    StructField("ano", IntegerType(), False),
    StructField("mes", IntegerType(), False),
    StructField("nome_mes", StringType(), False),
    StructField("trimestre", IntegerType(), False),
    StructField("decada", IntegerType(), False)
])

SCHEMA_DIM_PAIS_PRODUCAO = StructType([
    StructField("id_pais_producao", IntegerType(), False),
    StructField("pais_producao", StringType(), False)
])

SCHEMA_FATO_FILME = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_tempo", IntegerType(), False),
    StructField("receita", FloatType(), True),
    StructField("orcamento", FloatType(), True),
    StructField("nota_media", FloatType(), True),
    StructField("numero_votos", LongType(), True),
    StructField("popularidade_tmdb", FloatType(), True),
    StructField("duracao_minutos", IntegerType(), True)
])

SCHEMA_BRIDGE_FILME_GENERO = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_genero", IntegerType(), False)
])

SCHEMA_BRIDGE_FILME_PAIS = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_pais_producao", IntegerType(), False)
])

SCHEMA_BRIDGE_FILME_KEYWORD = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_keyword", IntegerType(), False)
])

# =============================================================================
# INICIALIZAÇÃO
# =============================================================================

args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 'TRUSTED_TMDB_PATH', 'TRUSTED_LOCAL_PATH', 'REFINED_BASE_PATH'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Aplica configurações do Spark
for config, value in SPARK_CONFIGS.items():
    spark.conf.set(config, value)

# Configura timezone
spark.conf.set("spark.sql.session.timeZone", "America/Sao_Paulo")

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def obter_caminhos_s3():
    """Retorna caminhos S3 das camadas"""
    return {
        'trusted_tmdb': args['TRUSTED_TMDB_PATH'],
        'trusted_local': args['TRUSTED_LOCAL_PATH'],
        'refined_movies': f"{args['REFINED_BASE_PATH']}/Movies"
    }

def obter_data_atual():
    """Retorna data atual formatada"""
    hoje = datetime.now()
    return {
        'ano': hoje.strftime('%Y'),
        'mes': hoje.strftime('%m'),
        'dia': hoje.strftime('%d')
    }

# =============================================================================
# FUNÇÕES DE LEITURA E CARREGAMENTO
# =============================================================================

def ler_dados_trusted():
    """Carrega dados das camadas Trusted"""
    caminhos = obter_caminhos_s3()
    
    # Carrega dados TMDB
    df_tmdb = spark.read.parquet(caminhos['trusted_tmdb'])
    df_tmdb = df_tmdb.repartition(PROCESSING_CONFIGS["particoes_iniciais"])
    df_tmdb.cache()
    
    # Carrega dados Local
    df_local = spark.read.parquet(caminhos['trusted_local'])
    df_local = df_local.repartition(PROCESSING_CONFIGS["particoes_iniciais"])
    df_local.cache()
    
    return df_tmdb, df_local

# =============================================================================
# FUNÇÕES DE FILTRAGEM E QUALIDADE
# =============================================================================

def filtrar_filmes_por_keywords(df_tmdb):
    """Filtra filmes por frequência de keywords (1%)"""
    
    total_filmes = df_tmdb.select('id_imdb').distinct().count()
    limite_minimo = int(total_filmes * PROCESSING_CONFIGS["limite_keyword_percentual"])
    
    df_keywords_validas = df_tmdb.filter(
        col('keyword').isNotNull() & 
        (trim(col('keyword')) != '') & 
        (trim(col('keyword')) != '#')
    ).select(
        col('keyword'),
        col('id_imdb')
    ) \
        .groupBy('keyword') \
        .agg(countDistinct('id_imdb').alias('freq_filmes')) \
        .filter(col('freq_filmes') >= limite_minimo) \
        .select('keyword')
    
    df_ids_filmes_validos = df_tmdb.filter(col('keyword').isNotNull()) \
        .select(
            col('keyword'),
            col('id_imdb')
        ) \
        .join(
            df_keywords_validas.select('keyword'),
            'keyword',
            'inner'
        ) \
        .select('id_imdb').distinct()
    
    df_filmes_paises = df_tmdb.alias('tmdb').join(
        df_ids_filmes_validos.alias('validos'),
        col('tmdb.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).select(
        col('tmdb.id_imdb'),
        col('tmdb.pais_producao')
    ).filter(col('pais_producao').isNotNull()).distinct()
    
    return df_ids_filmes_validos, df_keywords_validas, df_filmes_paises

def filtrar_filmes_validos(df_tmdb, df_local, df_ids_filmes_validos, df_keywords_validas):
    """Filtra filmes válidos em ambos os datasets"""
    
    df_tmdb_filtrado = df_tmdb.alias('tmdb').join(
        df_ids_filmes_validos.alias('validos'),
        col('tmdb.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).join(
        df_keywords_validas.select('keyword').alias('kw_validas'),
        col('tmdb.keyword') == col('kw_validas.keyword'),
        'inner'
    ).select(col('tmdb.*'))
    
    df_local_filtrado = df_local.alias('local').join(
        df_ids_filmes_validos.alias('validos'),
        col('local.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).select(col('local.*'))
    
    return df_tmdb_filtrado, df_local_filtrado

# =============================================================================
# FUNÇÕES DE TRANSFORMAÇÃO DE DADOS
# =============================================================================

def unificar_generos_complementar(df_local_filtrado, df_tmdb_filtrado):
    """Unifica gêneros do Local com complementos do TMDB"""
    
    df_local_base = df_local_filtrado.select('id_imdb', 'titulo_principal', 'duracao_minutos', 'nota_media', 'numero_votos', 'genero').cache()
    
    df_generos_tmdb = df_tmdb_filtrado.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero').alias('genero_tmdb')).distinct()
    
    df_generos_local = df_local_base.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero').alias('genero_local')).distinct()
    
    df_generos_novos = df_generos_tmdb.alias('tmdb').join(
        df_generos_local.alias('local'),
        (col('tmdb.id_imdb') == col('local.id_imdb')) & 
        (col('tmdb.genero_tmdb') == col('local.genero_local')),
        'left_anti'
    ).select(col('tmdb.id_imdb'), col('tmdb.genero_tmdb'))
    
    df_local_complementado = df_generos_novos.alias('novos').join(
        df_local_base.alias('base'),
        col('novos.id_imdb') == col('base.id_imdb'),
        'inner'
    ).select(
        col('novos.id_imdb'),
        col('base.titulo_principal'),
        col('base.duracao_minutos'),
        col('base.nota_media'),
        col('base.numero_votos'),
        col('novos.genero_tmdb').alias('genero')
    )
    
    df_local_base.unpersist()
    df_local_unificado = df_local_filtrado.unionByName(df_local_complementado, allowMissingColumns=True)
    
    df_tmdb_sem_genero = df_tmdb_filtrado.drop('genero')
    
    return df_local_unificado, df_tmdb_sem_genero

def padronizar_campos_string_tmdb(df_tmdb):
    """Padroniza campos string do TMDB"""
    # Renomeia coluna
    df_tmdb = df_tmdb.withColumnRenamed('production_countries', 'production_country')
    
    # Padroniza campos
    campos_string_tmdb = ['production_country', 'keywords']
    
    for campo in campos_string_tmdb:
        if campo in df_tmdb.columns:
            df_tmdb = df_tmdb.withColumn(
                campo,
                initcap(trim(col(campo)))
            )
    
    return df_tmdb

def padronizar_campos_string_local(df_local):
    """Padroniza campos string do Local com letra maiúscula"""
    campos_string_local = ['tituloPincipal']
    
    for campo in campos_string_local:
        if campo in df_local.columns:
            df_local = df_local.withColumn(
                campo,
                initcap(trim(col(campo)))
            )
    
    return df_local

def renomear_colunas_portugues_tmdb(df_tmdb):
    """Renomeia colunas do TMDB para português"""
    mapeamento_colunas = {
        'imdb_id': 'id_imdb',
        'revenue': 'receita',
        'budget': 'orcamento',
        'release_date': 'data_lancamento',
        'popularity': 'popularidade_tmdb',
        'adult': 'conteudo_adulto',
        'production_country': 'pais_producao',
        'keywords': 'keyword',
        'genres': 'genero'
    }
    
    for coluna_original, coluna_nova in mapeamento_colunas.items():
        if coluna_original in df_tmdb.columns:
            df_tmdb = df_tmdb.withColumnRenamed(coluna_original, coluna_nova)
    
    return df_tmdb

def renomear_colunas_portugues_local(df_local):
    """Renomeia colunas do Local para português"""
    mapeamento_colunas = {
        'id': 'id_imdb',
        'tituloPincipal': 'titulo_principal',
        'tempoMinutos': 'duracao_minutos',
        'notaMedia': 'nota_media',
        'numeroVotos': 'numero_votos'
    }
    
    for coluna_original, coluna_nova in mapeamento_colunas.items():
        if coluna_original in df_local.columns:
            df_local = df_local.withColumnRenamed(coluna_original, coluna_nova)
    
    return df_local

def reorganizar_ordem_colunas_tmdb(df_tmdb):
    """Reorganiza ordem das colunas do TMDB"""
    colunas_existentes = [col for col in COLUNAS_TMDB if col in df_tmdb.columns]
    return df_tmdb.select(colunas_existentes)

def reorganizar_ordem_colunas_local(df_local):
    """Reorganiza ordem das colunas do Local"""
    colunas_existentes = [col for col in COLUNAS_LOCAL if col in df_local.columns]
    return df_local.select(colunas_existentes)

# =============================================================================
# FUNÇÃO PRINCIPAL DE PROCESSAMENTO
# =============================================================================

def processar_dados_refined(df_tmdb, df_local):
    """Processa dados para a camada Refined"""
    
    print("1. Padronizando campos string...")
    df_tmdb_processado = padronizar_campos_string_tmdb(df_tmdb)
    df_local_processado = padronizar_campos_string_local(df_local)
    
    print("2. Renomeando colunas...")
    df_tmdb_processado = renomear_colunas_portugues_tmdb(df_tmdb_processado)
    df_local_processado = renomear_colunas_portugues_local(df_local_processado)
    
    print("3. Reorganizando colunas...")
    df_tmdb_processado = reorganizar_ordem_colunas_tmdb(df_tmdb_processado)
    df_local_processado = reorganizar_ordem_colunas_local(df_local_processado)
    
    print("4. Unificando gêneros...")
    df_local_unificado, df_tmdb_sem_genero = unificar_generos_complementar(df_local_processado, df_tmdb_processado)
    
    print("5. Filtrando filmes por frequência de keywords...")
    df_ids_filmes_validos, df_keywords_validas, df_filmes_paises = filtrar_filmes_por_keywords(df_tmdb_sem_genero)
    df_ids_filmes_validos.cache()
    df_filmes_paises.cache()
    
    print("6. Filtrando filmes e keywords válidas...")
    df_tmdb_filtrado, df_local_filtrado = filtrar_filmes_validos(df_tmdb_sem_genero, df_local_unificado, df_ids_filmes_validos, df_keywords_validas)
    
    df_tmdb_validos = df_tmdb_filtrado
    df_local_validos = df_local_filtrado
    
    df_tmdb_validos.cache()
    df_local_validos.cache()
    
    if df_tmdb_validos.rdd.getNumPartitions() > PROCESSING_CONFIGS["particoes_finais"]:
        df_tmdb_validos = df_tmdb_validos.coalesce(PROCESSING_CONFIGS["particoes_finais"])
    if df_local_validos.rdd.getNumPartitions() > PROCESSING_CONFIGS["particoes_finais"]:
        df_local_validos = df_local_validos.coalesce(PROCESSING_CONFIGS["particoes_finais"])
    
    return df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises

# =============================================================================
# FUNÇÕES DE MODELAGEM DIMENSIONAL
# =============================================================================

def criar_dim_filme(df_local_validos):
    """Cria dimensão de filmes APENAS dos filmes que passaram no filtro"""
    return df_local_validos.select(
        col('id_imdb'),
        col('titulo_principal')
    ).distinct().withColumn(
        'id_filme',
        row_number().over(Window.orderBy('id_imdb'))
    ).select(
        col('id_filme'),
        col('id_imdb'),
        col('titulo_principal')
    )

def criar_dim_genero(df_local_validos):
    """Cria dimensão de gêneros APENAS dos filmes que passaram no filtro"""
    return df_local_validos.filter(col('genero').isNotNull()) \
        .select('genero') \
        .distinct() \
        .withColumn(
            'id_genero',
            row_number().over(Window.orderBy('genero'))
        ).select(
            col('id_genero'),
            col('genero')
        )

def criar_dim_keyword(df_tmdb_validos, df_keywords_validas):
    """Cria dimensão de keywords"""
    return df_keywords_validas.select('keyword') \
        .distinct() \
        .withColumn(
            'id_keyword',
            row_number().over(Window.orderBy('keyword'))
        ).select(
            col('id_keyword'),
            col('keyword')
        )

def criar_dim_tempo(df_tmdb_validos):
    """Cria dimensão de tempo"""
    
    meses_pt = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    expr_mes = 'CASE'
    for num, nome in meses_pt.items():
        expr_mes += f" WHEN month(data_lancamento) = {num} THEN '{nome}'"
    expr_mes += " ELSE 'Desconhecido' END"
    
    return df_tmdb_validos.select(
        col('data_lancamento').cast('date')
    ).distinct().withColumn(
        'id_tempo',
        row_number().over(Window.orderBy('data_lancamento'))
    ).withColumn(
        'ano', year(col('data_lancamento')).cast('integer')
    ).withColumn(
        'mes', month(col('data_lancamento')).cast('integer')
    ).withColumn(
        'nome_mes', expr(expr_mes)
    ).withColumn(
        'trimestre', quarter(col('data_lancamento')).cast('integer')
    ).withColumn(
        'decada', floor(col('ano') / 10) * 10
    ).select(
        col('id_tempo').cast('integer'),
        col('data_lancamento').cast('date'),
        col('ano').cast('integer'),
        col('mes').cast('integer'),
        col('nome_mes').cast('string'),
        col('trimestre').cast('integer'),
        col('decada').cast('integer')
    )

def criar_dim_pais_producao(df_filmes_paises):
    """Cria dimensão de países produtores APENAS dos filmes que passaram no filtro"""
    return df_filmes_paises.select('pais_producao') \
        .distinct() \
        .withColumn(
            'id_pais_producao',
            row_number().over(Window.orderBy('pais_producao'))
        ).select(
            col('id_pais_producao'),
            col('pais_producao')
        )

def criar_bridge_filme_genero(df_local_validos, df_dim_genero, df_dim_filme):
    """Cria bridge table para relacionamento filme-gênero"""
    return df_local_validos.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero')) \
        .alias('local').join(
            df_dim_genero.alias('dim_genero'), 
            col('local.genero') == col('dim_genero.genero'), 
            'inner'
        ).join(
            df_dim_filme.alias('dim_filme'), 
            col('local.id_imdb') == col('dim_filme.id_imdb'), 
            'inner'
        ).select(col('dim_filme.id_filme'), col('dim_genero.id_genero')) \
        .distinct()

def criar_bridge_filme_pais(df_filmes_paises, df_dim_pais_producao, df_dim_filme):
    """Cria bridge table para relacionamento filme-país"""
    return df_filmes_paises.alias('filmes_paises').join(
        df_dim_pais_producao.alias('dim_pais'), 
        col('filmes_paises.pais_producao') == col('dim_pais.pais_producao'), 
        'inner'
    ).join(
        df_dim_filme.alias('dim_filme'), 
        col('filmes_paises.id_imdb') == col('dim_filme.id_imdb'), 
        'inner'
    ).select(col('dim_filme.id_filme'), col('dim_pais.id_pais_producao')) \
    .distinct()

def criar_bridge_filme_keyword(df_tmdb_validos, df_dim_keyword, df_dim_filme):
    """Cria bridge table para relacionamento filme-keyword"""
    
    df_bridge = df_tmdb_validos.filter(col('keyword').isNotNull()) \
        .select(col('id_imdb'), col('keyword')) \
        .alias('tmdb').join(
            df_dim_keyword.alias('dim_keyword'), 
            col('tmdb.keyword') == col('dim_keyword.keyword'), 
            'inner'
        ).join(
            df_dim_filme.alias('dim_filme'), 
            col('tmdb.id_imdb') == col('dim_filme.id_imdb'), 
            'inner'
        ).select(col('dim_filme.id_filme'), col('dim_keyword.id_keyword')) \
        .distinct()
    
    return df_bridge

def criar_fato_filme(df_tmdb_validos, df_local_validos, df_dim_filme, df_dim_tempo):
    """Cria tabela de fato com apenas chaves estrangeiras essenciais"""
    
    # Cria base com dados essenciais (um registro por filme)
    df_fato = df_tmdb_validos.alias('tmdb').join(
        df_dim_filme.alias('dim_filme'), 
        col('tmdb.id_imdb') == col('dim_filme.id_imdb'), 
        'inner'
    ).join(
        df_local_validos.alias('local'), 
        col('tmdb.id_imdb') == col('local.id_imdb'), 
        'inner'
    ).join(
        df_dim_tempo.alias('dim_tempo'), 
        col('tmdb.data_lancamento') == col('dim_tempo.data_lancamento'), 
        'inner'
    ).select(
        col('dim_filme.id_filme'), 
        col('dim_tempo.id_tempo'), 
        col('tmdb.receita').cast('float'),
        col('tmdb.orcamento').cast('float'),
        col('local.nota_media').cast('float'),
        col('local.numero_votos').cast('int'),
        col('tmdb.popularidade_tmdb').cast('float'),
        col('local.duracao_minutos').cast('int')
    ).distinct()
    
    return df_fato

def criar_modelagem_dimensional(df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises):
    """Cria modelagem dimensional completa"""
    
    df_dim_filme = criar_dim_filme(df_local_validos)
    df_dim_filme.cache()
    
    df_dim_genero = criar_dim_genero(df_local_validos)
    df_dim_genero.cache()
    
    df_dim_keyword = criar_dim_keyword(df_tmdb_validos, df_keywords_validas)
    df_dim_keyword.cache()
    
    df_dim_tempo = criar_dim_tempo(df_tmdb_validos)
    df_dim_tempo.cache()
    
    df_dim_pais_producao = criar_dim_pais_producao(df_filmes_paises)
    df_dim_pais_producao.cache()
    
    df_bridge_filme_genero = criar_bridge_filme_genero(df_local_validos, df_dim_genero, df_dim_filme)
    df_bridge_filme_pais = criar_bridge_filme_pais(df_filmes_paises, df_dim_pais_producao, df_dim_filme)
    df_bridge_filme_keyword = criar_bridge_filme_keyword(df_tmdb_validos, df_dim_keyword, df_dim_filme)
    
    df_fato_filme = criar_fato_filme(
        df_tmdb_validos, df_local_validos, df_dim_filme, df_dim_tempo
    )
    
    return {
        'tabelas_fato': {
            'fato_filme': df_fato_filme
        },
        'tabelas_dim': {
            'dim_filme': df_dim_filme,
            'dim_genero': df_dim_genero,
            'dim_keyword': df_dim_keyword,
            'dim_tempo': df_dim_tempo,
            'dim_pais_producao': df_dim_pais_producao
        },
        'tabelas_bridge': {
            'bridge_filme_genero': df_bridge_filme_genero,
            'bridge_filme_pais': df_bridge_filme_pais,
            'bridge_filme_keyword': df_bridge_filme_keyword
        }
    }

# =============================================================================
# FUNÇÕES DE SALVAMENTO
# =============================================================================

def salvar_tabela_sem_particao(df, caminho, nome_tabela):
    """Salva tabela sem particionamento"""
    schemas = {
        'dim_filme': SCHEMA_DIM_FILME,
        'dim_genero': SCHEMA_DIM_GENERO,
        'dim_keyword': SCHEMA_DIM_KEYWORD,
        'dim_tempo': SCHEMA_DIM_TEMPO,
        'dim_pais_producao': SCHEMA_DIM_PAIS_PRODUCAO
    }
    
    if nome_tabela in schemas:
        df = df.select(*schemas[nome_tabela].fieldNames())
    
    df.write \
        .mode("overwrite") \
        .option("compression", PROCESSING_CONFIGS["compression"]) \
        .option("maxRecordsPerFile", 100000) \
        .option("parquet.block.size", 128 * 1024 * 1024) \
        .parquet(f"{caminho}/{nome_tabela}")

def salvar_tabela_com_particao(df, caminho, nome_tabela, df_data_cache):
    """Salva tabela com particionamento"""
    
    df_com_tempo = df.alias('tabela').join(
        df_data_cache.alias('cache'),
        col('tabela.id_filme') == col('cache.id_filme'),
        'inner'
    )
    
    schemas = {
        'fato_filme': SCHEMA_FATO_FILME,
        'bridge_filme_genero': SCHEMA_BRIDGE_FILME_GENERO,
        'bridge_filme_pais': SCHEMA_BRIDGE_FILME_PAIS,
        'bridge_filme_keyword': SCHEMA_BRIDGE_FILME_KEYWORD
    }
    
    if nome_tabela in schemas:
        campos_com_tipos = [col(f'tabela.{field.name}').cast(field.dataType) for field in schemas[nome_tabela].fields]
        df_final = df_com_tempo.select(*campos_com_tipos, 'cache.ano', 'cache.mes')
    else:
        df_final = df_com_tempo.select('tabela.*', 'cache.ano', 'cache.mes')
    
    df_final.write \
        .partitionBy("ano", "mes") \
        .mode("overwrite") \
        .option("compression", PROCESSING_CONFIGS["compression"]) \
        .parquet(f"{caminho}/{nome_tabela}")

def salvar_modelagem_dimensional(modelagem):
    """Salva a modelagem dimensional na camada Refined"""
    caminhos = obter_caminhos_s3()
    data_atual = obter_data_atual()
    
    caminho_refined = f"{caminhos['refined_movies']}/{data_atual['ano']}/{data_atual['mes']}/{data_atual['dia']}"
    
    print(f"Salvando em: {caminho_refined}")
    
    print(f"\nVOLUME DE DADOS PARA SALVAMENTO:")
    
    print(f"\nDIMENSOES:")
    for nome_tabela, df in modelagem['tabelas_dim'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\nTABELAS DE FATO:")
    for nome_tabela, df in modelagem['tabelas_fato'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\nBRIDGE TABLES:")
    for nome_tabela, df in modelagem['tabelas_bridge'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\n" + "="*60)
    
    print("Salvando dimensões...")
    for nome_tabela, df in modelagem['tabelas_dim'].items():
        print(f"  - {nome_tabela}")
        salvar_tabela_sem_particao(df, caminho_refined, nome_tabela)
    
    print("Preparando cache de dados...")
    df_data_cache = modelagem['tabelas_fato']['fato_filme'].alias('fato').join(
        modelagem['tabelas_dim']['dim_tempo'].select('id_tempo', 'ano', 'mes').alias('tempo'),
        col('fato.id_tempo') == col('tempo.id_tempo'),
        'inner'
    ).select(
        col('fato.id_filme'),
        col('tempo.ano').cast('integer'),
        col('tempo.mes').cast('integer')
    ).repartition(10).cache()
    
    print("Salvando fato_filme...")
    salvar_tabela_com_particao(
        modelagem['tabelas_fato']['fato_filme'], 
        caminho_refined, 
        'fato_filme', 
        df_data_cache
    )
    
    print("Salvando bridge tables...")
    for nome_tabela, df in modelagem['tabelas_bridge'].items():
        print(f"  - {nome_tabela}")
        salvar_tabela_com_particao(
            df, 
            caminho_refined, 
            nome_tabela, 
            df_data_cache
        )
    
    df_data_cache.unpersist()

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do job Glue"""
    try:
        print("=== INICIANDO PROCESSAMENTO CAMADA REFINED ===")
        
        # =============================================================================
        # ETAPA 1: LEITURA DOS DADOS TRUSTED
        # =============================================================================
        print("1. Lendo dados da camada Trusted...")
        df_tmdb, df_local = ler_dados_trusted()
        
        # =============================================================================
        # ETAPA 2: PROCESSAMENTO DOS DADOS REFINED
        # =============================================================================
        print("2. Processando dados para camada Refined...")
        df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises = processar_dados_refined(df_tmdb, df_local)
        
        # =============================================================================
        # ETAPA 3: CRIAÇÃO DA MODELAGEM DIMENSIONAL
        # =============================================================================
        print("3. Criando modelagem dimensional...")
        modelagem = criar_modelagem_dimensional(df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises)
        
        # =============================================================================
        # ETAPA 4: SALVAMENTO DA MODELAGEM DIMENSIONAL
        # =============================================================================
        print("4. Salvando modelagem dimensional...")
        salvar_modelagem_dimensional(modelagem)
        
        # =============================================================================
        # ETAPA 5: LIMPEZA DE RECURSOS
        # =============================================================================
        print("5. Limpando recursos...")
        df_tmdb.unpersist()
        df_local.unpersist()
        
        # Limpa todos os DataFrames em cache
        spark.catalog.clearCache()
        
        print("=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"ERRO durante o processamento: {e}")
        raise
    finally:
        job.commit()

if __name__ == "__main__":
    main()
=======
#!/usr/bin/env python3
"""
Job AWS Glue para processamento da camada Refined
Processa dados da camada Trusted e cria modelagem dimensional
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
from datetime import datetime

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

# Configurações do Spark
SPARK_CONFIGS = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.localShuffleReader.enabled": "true",
    "spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold": "0",
    "spark.sql.adaptive.forceApply": "true",
    "spark.sql.adaptive.logLevel": "WARN"
}

# Configurações de processamento
PROCESSING_CONFIGS = {
    "particoes_iniciais": 10,
    "particoes_finais": 15,
    "limite_keyword_percentual": 0.01,
    "compression": "snappy"
}

# Colunas para reorganização
COLUNAS_TMDB = [
    'id_imdb', 'receita', 'orcamento', 'data_lancamento', 
    'popularidade_tmdb', 'genero', 'conteudo_adulto', 'pais_producao', 'keyword'
]

COLUNAS_LOCAL = [
    'id_imdb', 'titulo_principal', 'genero', 
    'duracao_minutos', 'nota_media', 'numero_votos'
]

# Schemas explícitos para garantir tipos consistentes
SCHEMA_DIM_FILME = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_imdb", StringType(), False),
    StructField("titulo_principal", StringType(), True)
])

SCHEMA_DIM_GENERO = StructType([
    StructField("id_genero", IntegerType(), False),
    StructField("genero", StringType(), False)
])

SCHEMA_DIM_KEYWORD = StructType([
    StructField("id_keyword", IntegerType(), False),
    StructField("keyword", StringType(), False)
])

SCHEMA_DIM_TEMPO = StructType([
    StructField("id_tempo", IntegerType(), False),
    StructField("data_lancamento", DateType(), False),
    StructField("ano", IntegerType(), False),
    StructField("mes", IntegerType(), False),
    StructField("nome_mes", StringType(), False),
    StructField("trimestre", IntegerType(), False),
    StructField("decada", IntegerType(), False)
])

SCHEMA_DIM_PAIS_PRODUCAO = StructType([
    StructField("id_pais_producao", IntegerType(), False),
    StructField("pais_producao", StringType(), False)
])

SCHEMA_FATO_FILME = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_tempo", IntegerType(), False),
    StructField("receita", FloatType(), True),
    StructField("orcamento", FloatType(), True),
    StructField("nota_media", FloatType(), True),
    StructField("numero_votos", LongType(), True),
    StructField("popularidade_tmdb", FloatType(), True),
    StructField("duracao_minutos", IntegerType(), True)
])

SCHEMA_BRIDGE_FILME_GENERO = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_genero", IntegerType(), False)
])

SCHEMA_BRIDGE_FILME_PAIS = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_pais_producao", IntegerType(), False)
])

SCHEMA_BRIDGE_FILME_KEYWORD = StructType([
    StructField("id_filme", IntegerType(), False),
    StructField("id_keyword", IntegerType(), False)
])

# =============================================================================
# INICIALIZAÇÃO
# =============================================================================

args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 'TRUSTED_TMDB_PATH', 'TRUSTED_LOCAL_PATH', 'REFINED_BASE_PATH'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Aplica configurações do Spark
for config, value in SPARK_CONFIGS.items():
    spark.conf.set(config, value)

# Configura timezone
spark.conf.set("spark.sql.session.timeZone", "America/Sao_Paulo")

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def obter_caminhos_s3():
    """Retorna caminhos S3 das camadas"""
    return {
        'trusted_tmdb': args['TRUSTED_TMDB_PATH'],
        'trusted_local': args['TRUSTED_LOCAL_PATH'],
        'refined_movies': f"{args['REFINED_BASE_PATH']}/Movies"
    }

def obter_data_atual():
    """Retorna data atual formatada"""
    hoje = datetime.now()
    return {
        'ano': hoje.strftime('%Y'),
        'mes': hoje.strftime('%m'),
        'dia': hoje.strftime('%d')
    }

# =============================================================================
# FUNÇÕES DE LEITURA E CARREGAMENTO
# =============================================================================

def ler_dados_trusted():
    """Carrega dados das camadas Trusted"""
    caminhos = obter_caminhos_s3()
    
    # Carrega dados TMDB
    df_tmdb = spark.read.parquet(caminhos['trusted_tmdb'])
    df_tmdb = df_tmdb.repartition(PROCESSING_CONFIGS["particoes_iniciais"])
    df_tmdb.cache()
    
    # Carrega dados Local
    df_local = spark.read.parquet(caminhos['trusted_local'])
    df_local = df_local.repartition(PROCESSING_CONFIGS["particoes_iniciais"])
    df_local.cache()
    
    return df_tmdb, df_local

# =============================================================================
# FUNÇÕES DE FILTRAGEM E QUALIDADE
# =============================================================================

def filtrar_filmes_por_keywords(df_tmdb):
    """Filtra filmes por frequência de keywords (1%)"""
    
    total_filmes = df_tmdb.select('id_imdb').distinct().count()
    limite_minimo = int(total_filmes * PROCESSING_CONFIGS["limite_keyword_percentual"])
    
    df_keywords_validas = df_tmdb.filter(
        col('keyword').isNotNull() & 
        (trim(col('keyword')) != '') & 
        (trim(col('keyword')) != '#')
    ).select(
        col('keyword'),
        col('id_imdb')
    ) \
        .groupBy('keyword') \
        .agg(countDistinct('id_imdb').alias('freq_filmes')) \
        .filter(col('freq_filmes') >= limite_minimo) \
        .select('keyword')
    
    df_ids_filmes_validos = df_tmdb.filter(col('keyword').isNotNull()) \
        .select(
            col('keyword'),
            col('id_imdb')
        ) \
        .join(
            df_keywords_validas.select('keyword'),
            'keyword',
            'inner'
        ) \
        .select('id_imdb').distinct()
    
    df_filmes_paises = df_tmdb.alias('tmdb').join(
        df_ids_filmes_validos.alias('validos'),
        col('tmdb.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).select(
        col('tmdb.id_imdb'),
        col('tmdb.pais_producao')
    ).filter(col('pais_producao').isNotNull()).distinct()
    
    return df_ids_filmes_validos, df_keywords_validas, df_filmes_paises

def filtrar_filmes_validos(df_tmdb, df_local, df_ids_filmes_validos, df_keywords_validas):
    """Filtra filmes válidos em ambos os datasets"""
    
    df_tmdb_filtrado = df_tmdb.alias('tmdb').join(
        df_ids_filmes_validos.alias('validos'),
        col('tmdb.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).join(
        df_keywords_validas.select('keyword').alias('kw_validas'),
        col('tmdb.keyword') == col('kw_validas.keyword'),
        'inner'
    ).select(col('tmdb.*'))
    
    df_local_filtrado = df_local.alias('local').join(
        df_ids_filmes_validos.alias('validos'),
        col('local.id_imdb') == col('validos.id_imdb'),
        'inner'
    ).select(col('local.*'))
    
    return df_tmdb_filtrado, df_local_filtrado

# =============================================================================
# FUNÇÕES DE TRANSFORMAÇÃO DE DADOS
# =============================================================================

def unificar_generos_complementar(df_local_filtrado, df_tmdb_filtrado):
    """Unifica gêneros do Local com complementos do TMDB"""
    
    df_local_base = df_local_filtrado.select('id_imdb', 'titulo_principal', 'duracao_minutos', 'nota_media', 'numero_votos', 'genero').cache()
    
    df_generos_tmdb = df_tmdb_filtrado.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero').alias('genero_tmdb')).distinct()
    
    df_generos_local = df_local_base.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero').alias('genero_local')).distinct()
    
    df_generos_novos = df_generos_tmdb.alias('tmdb').join(
        df_generos_local.alias('local'),
        (col('tmdb.id_imdb') == col('local.id_imdb')) & 
        (col('tmdb.genero_tmdb') == col('local.genero_local')),
        'left_anti'
    ).select(col('tmdb.id_imdb'), col('tmdb.genero_tmdb'))
    
    df_local_complementado = df_generos_novos.alias('novos').join(
        df_local_base.alias('base'),
        col('novos.id_imdb') == col('base.id_imdb'),
        'inner'
    ).select(
        col('novos.id_imdb'),
        col('base.titulo_principal'),
        col('base.duracao_minutos'),
        col('base.nota_media'),
        col('base.numero_votos'),
        col('novos.genero_tmdb').alias('genero')
    )
    
    df_local_base.unpersist()
    df_local_unificado = df_local_filtrado.unionByName(df_local_complementado, allowMissingColumns=True)
    
    df_tmdb_sem_genero = df_tmdb_filtrado.drop('genero')
    
    return df_local_unificado, df_tmdb_sem_genero

def padronizar_campos_string_tmdb(df_tmdb):
    """Padroniza campos string do TMDB"""
    # Renomeia coluna
    df_tmdb = df_tmdb.withColumnRenamed('production_countries', 'production_country')
    
    # Padroniza campos
    campos_string_tmdb = ['production_country', 'keywords']
    
    for campo in campos_string_tmdb:
        if campo in df_tmdb.columns:
            df_tmdb = df_tmdb.withColumn(
                campo,
                initcap(trim(col(campo)))
            )
    
    return df_tmdb

def padronizar_campos_string_local(df_local):
    """Padroniza campos string do Local com letra maiúscula"""
    campos_string_local = ['tituloPincipal']
    
    for campo in campos_string_local:
        if campo in df_local.columns:
            df_local = df_local.withColumn(
                campo,
                initcap(trim(col(campo)))
            )
    
    return df_local

def renomear_colunas_portugues_tmdb(df_tmdb):
    """Renomeia colunas do TMDB para português"""
    mapeamento_colunas = {
        'imdb_id': 'id_imdb',
        'revenue': 'receita',
        'budget': 'orcamento',
        'release_date': 'data_lancamento',
        'popularity': 'popularidade_tmdb',
        'adult': 'conteudo_adulto',
        'production_country': 'pais_producao',
        'keywords': 'keyword',
        'genres': 'genero'
    }
    
    for coluna_original, coluna_nova in mapeamento_colunas.items():
        if coluna_original in df_tmdb.columns:
            df_tmdb = df_tmdb.withColumnRenamed(coluna_original, coluna_nova)
    
    return df_tmdb

def renomear_colunas_portugues_local(df_local):
    """Renomeia colunas do Local para português"""
    mapeamento_colunas = {
        'id': 'id_imdb',
        'tituloPincipal': 'titulo_principal',
        'tempoMinutos': 'duracao_minutos',
        'notaMedia': 'nota_media',
        'numeroVotos': 'numero_votos'
    }
    
    for coluna_original, coluna_nova in mapeamento_colunas.items():
        if coluna_original in df_local.columns:
            df_local = df_local.withColumnRenamed(coluna_original, coluna_nova)
    
    return df_local

def reorganizar_ordem_colunas_tmdb(df_tmdb):
    """Reorganiza ordem das colunas do TMDB"""
    colunas_existentes = [col for col in COLUNAS_TMDB if col in df_tmdb.columns]
    return df_tmdb.select(colunas_existentes)

def reorganizar_ordem_colunas_local(df_local):
    """Reorganiza ordem das colunas do Local"""
    colunas_existentes = [col for col in COLUNAS_LOCAL if col in df_local.columns]
    return df_local.select(colunas_existentes)

# =============================================================================
# FUNÇÃO PRINCIPAL DE PROCESSAMENTO
# =============================================================================

def processar_dados_refined(df_tmdb, df_local):
    """Processa dados para a camada Refined"""
    
    print("1. Padronizando campos string...")
    df_tmdb_processado = padronizar_campos_string_tmdb(df_tmdb)
    df_local_processado = padronizar_campos_string_local(df_local)
    
    print("2. Renomeando colunas...")
    df_tmdb_processado = renomear_colunas_portugues_tmdb(df_tmdb_processado)
    df_local_processado = renomear_colunas_portugues_local(df_local_processado)
    
    print("3. Reorganizando colunas...")
    df_tmdb_processado = reorganizar_ordem_colunas_tmdb(df_tmdb_processado)
    df_local_processado = reorganizar_ordem_colunas_local(df_local_processado)
    
    print("4. Unificando gêneros...")
    df_local_unificado, df_tmdb_sem_genero = unificar_generos_complementar(df_local_processado, df_tmdb_processado)
    
    print("5. Filtrando filmes por frequência de keywords...")
    df_ids_filmes_validos, df_keywords_validas, df_filmes_paises = filtrar_filmes_por_keywords(df_tmdb_sem_genero)
    df_ids_filmes_validos.cache()
    df_filmes_paises.cache()
    
    print("6. Filtrando filmes e keywords válidas...")
    df_tmdb_filtrado, df_local_filtrado = filtrar_filmes_validos(df_tmdb_sem_genero, df_local_unificado, df_ids_filmes_validos, df_keywords_validas)
    
    df_tmdb_validos = df_tmdb_filtrado
    df_local_validos = df_local_filtrado
    
    df_tmdb_validos.cache()
    df_local_validos.cache()
    
    if df_tmdb_validos.rdd.getNumPartitions() > PROCESSING_CONFIGS["particoes_finais"]:
        df_tmdb_validos = df_tmdb_validos.coalesce(PROCESSING_CONFIGS["particoes_finais"])
    if df_local_validos.rdd.getNumPartitions() > PROCESSING_CONFIGS["particoes_finais"]:
        df_local_validos = df_local_validos.coalesce(PROCESSING_CONFIGS["particoes_finais"])
    
    return df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises

# =============================================================================
# FUNÇÕES DE MODELAGEM DIMENSIONAL
# =============================================================================

def criar_dim_filme(df_local_validos):
    """Cria dimensão de filmes APENAS dos filmes que passaram no filtro"""
    return df_local_validos.select(
        col('id_imdb'),
        col('titulo_principal')
    ).distinct().withColumn(
        'id_filme',
        row_number().over(Window.orderBy('id_imdb'))
    ).select(
        col('id_filme'),
        col('id_imdb'),
        col('titulo_principal')
    )

def criar_dim_genero(df_local_validos):
    """Cria dimensão de gêneros APENAS dos filmes que passaram no filtro"""
    return df_local_validos.filter(col('genero').isNotNull()) \
        .select('genero') \
        .distinct() \
        .withColumn(
            'id_genero',
            row_number().over(Window.orderBy('genero'))
        ).select(
            col('id_genero'),
            col('genero')
        )

def criar_dim_keyword(df_tmdb_validos, df_keywords_validas):
    """Cria dimensão de keywords"""
    return df_keywords_validas.select('keyword') \
        .distinct() \
        .withColumn(
            'id_keyword',
            row_number().over(Window.orderBy('keyword'))
        ).select(
            col('id_keyword'),
            col('keyword')
        )

def criar_dim_tempo(df_tmdb_validos):
    """Cria dimensão de tempo"""
    
    meses_pt = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    expr_mes = 'CASE'
    for num, nome in meses_pt.items():
        expr_mes += f" WHEN month(data_lancamento) = {num} THEN '{nome}'"
    expr_mes += " ELSE 'Desconhecido' END"
    
    return df_tmdb_validos.select(
        col('data_lancamento').cast('date')
    ).distinct().withColumn(
        'id_tempo',
        row_number().over(Window.orderBy('data_lancamento'))
    ).withColumn(
        'ano', year(col('data_lancamento')).cast('integer')
    ).withColumn(
        'mes', month(col('data_lancamento')).cast('integer')
    ).withColumn(
        'nome_mes', expr(expr_mes)
    ).withColumn(
        'trimestre', quarter(col('data_lancamento')).cast('integer')
    ).withColumn(
        'decada', floor(col('ano') / 10) * 10
    ).select(
        col('id_tempo').cast('integer'),
        col('data_lancamento').cast('date'),
        col('ano').cast('integer'),
        col('mes').cast('integer'),
        col('nome_mes').cast('string'),
        col('trimestre').cast('integer'),
        col('decada').cast('integer')
    )

def criar_dim_pais_producao(df_filmes_paises):
    """Cria dimensão de países produtores APENAS dos filmes que passaram no filtro"""
    return df_filmes_paises.select('pais_producao') \
        .distinct() \
        .withColumn(
            'id_pais_producao',
            row_number().over(Window.orderBy('pais_producao'))
        ).select(
            col('id_pais_producao'),
            col('pais_producao')
        )

def criar_bridge_filme_genero(df_local_validos, df_dim_genero, df_dim_filme):
    """Cria bridge table para relacionamento filme-gênero"""
    return df_local_validos.filter(col('genero').isNotNull()) \
        .select(col('id_imdb'), col('genero')) \
        .alias('local').join(
            df_dim_genero.alias('dim_genero'), 
            col('local.genero') == col('dim_genero.genero'), 
            'inner'
        ).join(
            df_dim_filme.alias('dim_filme'), 
            col('local.id_imdb') == col('dim_filme.id_imdb'), 
            'inner'
        ).select(col('dim_filme.id_filme'), col('dim_genero.id_genero')) \
        .distinct()

def criar_bridge_filme_pais(df_filmes_paises, df_dim_pais_producao, df_dim_filme):
    """Cria bridge table para relacionamento filme-país"""
    return df_filmes_paises.alias('filmes_paises').join(
        df_dim_pais_producao.alias('dim_pais'), 
        col('filmes_paises.pais_producao') == col('dim_pais.pais_producao'), 
        'inner'
    ).join(
        df_dim_filme.alias('dim_filme'), 
        col('filmes_paises.id_imdb') == col('dim_filme.id_imdb'), 
        'inner'
    ).select(col('dim_filme.id_filme'), col('dim_pais.id_pais_producao')) \
    .distinct()

def criar_bridge_filme_keyword(df_tmdb_validos, df_dim_keyword, df_dim_filme):
    """Cria bridge table para relacionamento filme-keyword"""
    
    df_bridge = df_tmdb_validos.filter(col('keyword').isNotNull()) \
        .select(col('id_imdb'), col('keyword')) \
        .alias('tmdb').join(
            df_dim_keyword.alias('dim_keyword'), 
            col('tmdb.keyword') == col('dim_keyword.keyword'), 
            'inner'
        ).join(
            df_dim_filme.alias('dim_filme'), 
            col('tmdb.id_imdb') == col('dim_filme.id_imdb'), 
            'inner'
        ).select(col('dim_filme.id_filme'), col('dim_keyword.id_keyword')) \
        .distinct()
    
    return df_bridge

def criar_fato_filme(df_tmdb_validos, df_local_validos, df_dim_filme, df_dim_tempo):
    """Cria tabela de fato com apenas chaves estrangeiras essenciais"""
    
    # Cria base com dados essenciais (um registro por filme)
    df_fato = df_tmdb_validos.alias('tmdb').join(
        df_dim_filme.alias('dim_filme'), 
        col('tmdb.id_imdb') == col('dim_filme.id_imdb'), 
        'inner'
    ).join(
        df_local_validos.alias('local'), 
        col('tmdb.id_imdb') == col('local.id_imdb'), 
        'inner'
    ).join(
        df_dim_tempo.alias('dim_tempo'), 
        col('tmdb.data_lancamento') == col('dim_tempo.data_lancamento'), 
        'inner'
    ).select(
        col('dim_filme.id_filme'), 
        col('dim_tempo.id_tempo'), 
        col('tmdb.receita').cast('float'),
        col('tmdb.orcamento').cast('float'),
        col('local.nota_media').cast('float'),
        col('local.numero_votos').cast('int'),
        col('tmdb.popularidade_tmdb').cast('float'),
        col('local.duracao_minutos').cast('int')
    ).distinct()
    
    return df_fato

def criar_modelagem_dimensional(df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises):
    """Cria modelagem dimensional completa"""
    
    df_dim_filme = criar_dim_filme(df_local_validos)
    df_dim_filme.cache()
    
    df_dim_genero = criar_dim_genero(df_local_validos)
    df_dim_genero.cache()
    
    df_dim_keyword = criar_dim_keyword(df_tmdb_validos, df_keywords_validas)
    df_dim_keyword.cache()
    
    df_dim_tempo = criar_dim_tempo(df_tmdb_validos)
    df_dim_tempo.cache()
    
    df_dim_pais_producao = criar_dim_pais_producao(df_filmes_paises)
    df_dim_pais_producao.cache()
    
    df_bridge_filme_genero = criar_bridge_filme_genero(df_local_validos, df_dim_genero, df_dim_filme)
    df_bridge_filme_pais = criar_bridge_filme_pais(df_filmes_paises, df_dim_pais_producao, df_dim_filme)
    df_bridge_filme_keyword = criar_bridge_filme_keyword(df_tmdb_validos, df_dim_keyword, df_dim_filme)
    
    df_fato_filme = criar_fato_filme(
        df_tmdb_validos, df_local_validos, df_dim_filme, df_dim_tempo
    )
    
    return {
        'tabelas_fato': {
            'fato_filme': df_fato_filme
        },
        'tabelas_dim': {
            'dim_filme': df_dim_filme,
            'dim_genero': df_dim_genero,
            'dim_keyword': df_dim_keyword,
            'dim_tempo': df_dim_tempo,
            'dim_pais_producao': df_dim_pais_producao
        },
        'tabelas_bridge': {
            'bridge_filme_genero': df_bridge_filme_genero,
            'bridge_filme_pais': df_bridge_filme_pais,
            'bridge_filme_keyword': df_bridge_filme_keyword
        }
    }

# =============================================================================
# FUNÇÕES DE SALVAMENTO
# =============================================================================

def salvar_tabela_sem_particao(df, caminho, nome_tabela):
    """Salva tabela sem particionamento"""
    schemas = {
        'dim_filme': SCHEMA_DIM_FILME,
        'dim_genero': SCHEMA_DIM_GENERO,
        'dim_keyword': SCHEMA_DIM_KEYWORD,
        'dim_tempo': SCHEMA_DIM_TEMPO,
        'dim_pais_producao': SCHEMA_DIM_PAIS_PRODUCAO
    }
    
    if nome_tabela in schemas:
        df = df.select(*schemas[nome_tabela].fieldNames())
    
    df.write \
        .mode("overwrite") \
        .option("compression", PROCESSING_CONFIGS["compression"]) \
        .option("maxRecordsPerFile", 100000) \
        .option("parquet.block.size", 128 * 1024 * 1024) \
        .parquet(f"{caminho}/{nome_tabela}")

def salvar_tabela_com_particao(df, caminho, nome_tabela, df_data_cache):
    """Salva tabela com particionamento"""
    
    df_com_tempo = df.alias('tabela').join(
        df_data_cache.alias('cache'),
        col('tabela.id_filme') == col('cache.id_filme'),
        'inner'
    )
    
    schemas = {
        'fato_filme': SCHEMA_FATO_FILME,
        'bridge_filme_genero': SCHEMA_BRIDGE_FILME_GENERO,
        'bridge_filme_pais': SCHEMA_BRIDGE_FILME_PAIS,
        'bridge_filme_keyword': SCHEMA_BRIDGE_FILME_KEYWORD
    }
    
    if nome_tabela in schemas:
        campos_com_tipos = [col(f'tabela.{field.name}').cast(field.dataType) for field in schemas[nome_tabela].fields]
        df_final = df_com_tempo.select(*campos_com_tipos, 'cache.ano', 'cache.mes')
    else:
        df_final = df_com_tempo.select('tabela.*', 'cache.ano', 'cache.mes')
    
    df_final.write \
        .partitionBy("ano", "mes") \
        .mode("overwrite") \
        .option("compression", PROCESSING_CONFIGS["compression"]) \
        .parquet(f"{caminho}/{nome_tabela}")

def salvar_modelagem_dimensional(modelagem):
    """Salva a modelagem dimensional na camada Refined"""
    caminhos = obter_caminhos_s3()
    data_atual = obter_data_atual()
    
    caminho_refined = f"{caminhos['refined_movies']}/{data_atual['ano']}/{data_atual['mes']}/{data_atual['dia']}"
    
    print(f"Salvando em: {caminho_refined}")
    
    print(f"\nVOLUME DE DADOS PARA SALVAMENTO:")
    
    print(f"\nDIMENSOES:")
    for nome_tabela, df in modelagem['tabelas_dim'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\nTABELAS DE FATO:")
    for nome_tabela, df in modelagem['tabelas_fato'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\nBRIDGE TABLES:")
    for nome_tabela, df in modelagem['tabelas_bridge'].items():
        registros = df.count()
        print(f"  - {nome_tabela}: {registros:,} registros")
    
    print(f"\n" + "="*60)
    
    print("Salvando dimensões...")
    for nome_tabela, df in modelagem['tabelas_dim'].items():
        print(f"  - {nome_tabela}")
        salvar_tabela_sem_particao(df, caminho_refined, nome_tabela)
    
    print("Preparando cache de dados...")
    df_data_cache = modelagem['tabelas_fato']['fato_filme'].alias('fato').join(
        modelagem['tabelas_dim']['dim_tempo'].select('id_tempo', 'ano', 'mes').alias('tempo'),
        col('fato.id_tempo') == col('tempo.id_tempo'),
        'inner'
    ).select(
        col('fato.id_filme'),
        col('tempo.ano').cast('integer'),
        col('tempo.mes').cast('integer')
    ).repartition(10).cache()
    
    print("Salvando fato_filme...")
    salvar_tabela_com_particao(
        modelagem['tabelas_fato']['fato_filme'], 
        caminho_refined, 
        'fato_filme', 
        df_data_cache
    )
    
    print("Salvando bridge tables...")
    for nome_tabela, df in modelagem['tabelas_bridge'].items():
        print(f"  - {nome_tabela}")
        salvar_tabela_com_particao(
            df, 
            caminho_refined, 
            nome_tabela, 
            df_data_cache
        )
    
    df_data_cache.unpersist()

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do job Glue"""
    try:
        print("=== INICIANDO PROCESSAMENTO CAMADA REFINED ===")
        
        # =============================================================================
        # ETAPA 1: LEITURA DOS DADOS TRUSTED
        # =============================================================================
        print("1. Lendo dados da camada Trusted...")
        df_tmdb, df_local = ler_dados_trusted()
        
        # =============================================================================
        # ETAPA 2: PROCESSAMENTO DOS DADOS REFINED
        # =============================================================================
        print("2. Processando dados para camada Refined...")
        df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises = processar_dados_refined(df_tmdb, df_local)
        
        # =============================================================================
        # ETAPA 3: CRIAÇÃO DA MODELAGEM DIMENSIONAL
        # =============================================================================
        print("3. Criando modelagem dimensional...")
        modelagem = criar_modelagem_dimensional(df_tmdb_validos, df_local_validos, df_keywords_validas, df_filmes_paises)
        
        # =============================================================================
        # ETAPA 4: SALVAMENTO DA MODELAGEM DIMENSIONAL
        # =============================================================================
        print("4. Salvando modelagem dimensional...")
        salvar_modelagem_dimensional(modelagem)
        
        # =============================================================================
        # ETAPA 5: LIMPEZA DE RECURSOS
        # =============================================================================
        print("5. Limpando recursos...")
        df_tmdb.unpersist()
        df_local.unpersist()
        
        # Limpa todos os DataFrames em cache
        spark.catalog.clearCache()
        
        print("=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"ERRO durante o processamento: {e}")
        raise
    finally:
        job.commit()

if __name__ == "__main__":
    main()
>>>>>>> 53748dd930b2c36edb9b3adbda3e293b1e4298e3
