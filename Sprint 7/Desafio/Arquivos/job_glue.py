import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

from pyspark.context import SparkContext
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col, row_number, explode, lit, split, element_at, when
)


# Captura os parâmetros de entrada do job
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_TRUSTED_LOCAL', 'S3_TRUSTED_TMDB', 'S3_TARGET_BASE_PATH'])

# Inicializa contexto Spark e Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Configurações para desabilitar otimizações automáticas no Spark
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

# Leitura dos dados parquet das áreas trusted (local e TMDB)
df_local = spark.read.parquet(args['S3_TRUSTED_LOCAL'])
df_tmdb = spark.read.parquet(args['S3_TRUSTED_TMDB'])

# Renomeia colunas para evitar conflito no join
df_local = df_local.withColumnRenamed("id", "imdb_id_local")
df_tmdb = df_tmdb.withColumnRenamed("imdb_id", "imdb_id_tmdb")

# Realiza join entre dados locais e TMDB pelo imdb_id
df = df_local.join(df_tmdb, df_local.imdb_id_local == df_tmdb.imdb_id_tmdb, how="inner")

# --- DIMENSÃO TEMPO ---

# Seleciona e remove duplicatas de ano e mês de lançamento
dim_tempo_df = df.select(
    col("ano_lancamento"),
    col("mes_lancamento")
).dropDuplicates()

# Mapeia o nome do mês conforme o número
dim_tempo_df = dim_tempo_df.withColumn(
    "nome_mes",
    when(col("mes_lancamento") == 1, "Janeiro")
    .when(col("mes_lancamento") == 2, "Fevereiro")
    .when(col("mes_lancamento") == 3, "Março")
    .when(col("mes_lancamento") == 4, "Abril")
    .when(col("mes_lancamento") == 5, "Maio")
    .when(col("mes_lancamento") == 6, "Junho")
    .when(col("mes_lancamento") == 7, "Julho")
    .when(col("mes_lancamento") == 8, "Agosto")
    .when(col("mes_lancamento") == 9, "Setembro")
    .when(col("mes_lancamento") == 10, "Outubro")
    .when(col("mes_lancamento") == 11, "Novembro")
    .when(col("mes_lancamento") == 12, "Dezembro")
    .otherwise(None)
)

# Define trimestre do ano para cada mês
dim_tempo_df = dim_tempo_df.withColumn(
    "trimestre",
    when(col("mes_lancamento").between(1, 3), 1)
    .when(col("mes_lancamento").between(4, 6), 2)
    .when(col("mes_lancamento").between(7, 9), 3)
    .when(col("mes_lancamento").between(10, 12), 4)
    .otherwise(None)
)

# Define semestre do ano para cada mês
dim_tempo_df = dim_tempo_df.withColumn(
    "semestre",
    when(col("mes_lancamento") <= 6, 1).otherwise(2)
)

# Define se o mês está em período de férias
dim_tempo_df = dim_tempo_df.withColumn(
    "eh_ferias",
    col("mes_lancamento").isin([1, 6, 7, 12])
)

# Cria chave surrogate para dimensão tempo
window_tempo = Window.orderBy("ano_lancamento", "mes_lancamento")
dim_tempo_df = dim_tempo_df.withColumn("tempo_id", row_number().over(window_tempo))

# --- DIMENSÃO FILME ---

# Seleciona e remove duplicatas dos filmes
dim_filme_df = df.select(
    col("imdb_id_local").alias("imdb_id"),
    col("tituloprincipal"),
    col("titulobr"),
    col("genero"),
    col("tempominutos"),
    col("adult").alias("eh_adulto"),
    col("ano_lancamento"),
    col("mes_lancamento")
).dropDuplicates()

# Cria chave surrogate para dimensão filme
window_filme = Window.orderBy("imdb_id")
dim_filme_df = dim_filme_df.withColumn("filme_id", row_number().over(window_filme))

# --- DIMENSÃO ARTISTA PRINCIPAL ---

# Converte string com títulos separados por vírgula em array
df = df.withColumn("titulosmaisconhecidos_array", split(col("titulosmaisconhecidos"), ","))

# Extrai até 4 filmes conhecidos do artista
df = df.withColumn("filme_imdb_id_top1", element_at(col("titulosmaisconhecidos_array"), 1)) \
       .withColumn("filme_imdb_id_top2", element_at(col("titulosmaisconhecidos_array"), 2)) \
       .withColumn("filme_imdb_id_top3", element_at(col("titulosmaisconhecidos_array"), 3)) \
       .withColumn("filme_imdb_id_top4", element_at(col("titulosmaisconhecidos_array"), 4))

# Seleciona dados dos artistas e remove duplicatas
dim_artista_df = df.select(
    col("nomeartista"),
    col("generoartista"),
    col("filme_imdb_id_top1"),
    col("filme_imdb_id_top2"),
    col("filme_imdb_id_top3"),
    col("filme_imdb_id_top4")
).dropDuplicates()

# Cria chave surrogate para artista principal
window_artista = Window.orderBy("nomeartista")
dim_artista_df = dim_artista_df.withColumn("artista_principal_id", row_number().over(window_artista))

# --- DIMENSÃO PRODUTORA ---

# Transforma cada país do array em uma linha separada e remove duplicatas
produtoras_exploded = df.select(explode(col("prod_countries")).alias("pais_origem")).dropDuplicates()

# Cria chave surrogate para produtoras
window_produtora = Window.orderBy("pais_origem")
dim_produtora_df = produtoras_exploded.withColumn("produtora_id", row_number().over(window_produtora))

# Seleção de chaves surrogate para joins
dim_filme_keys = dim_filme_df.select("imdb_id", "filme_id", "ano_lancamento", "mes_lancamento")
dim_tempo_keys = dim_tempo_df.select("ano_lancamento", "mes_lancamento", "tempo_id")
dim_artista_keys = dim_artista_df.select("nomeartista", "artista_principal_id")
dim_produtora_keys = dim_produtora_df.select("pais_origem", "produtora_id")

# Prepara colunas produtoras para o fato
df = df.withColumn("prod_countries_array", col("prod_countries"))
df = df.withColumn("produtora1", element_at(col("prod_countries_array"), 1)) \
       .withColumn("produtora2", element_at(col("prod_countries_array"), 2)) \
       .withColumn("produtora3", element_at(col("prod_countries_array"), 3))

# Faz join para obter os ids das produtoras
df = df.join(dim_produtora_keys.withColumnRenamed("pais_origem", "produtora1"), "produtora1", "left") \
       .withColumnRenamed("produtora_id", "produtora1_id")

df = df.join(dim_produtora_keys.withColumnRenamed("pais_origem", "produtora2"), "produtora2", "left") \
       .withColumnRenamed("produtora_id", "produtora2_id")

df = df.join(dim_produtora_keys.withColumnRenamed("pais_origem", "produtora3"), "produtora3", "left") \
       .withColumnRenamed("produtora_id", "produtora3_id")

# Montagem da tabela fato
df_alias = df.alias("df")
dim_filme_keys_alias = dim_filme_keys.alias("filme")
dim_tempo_keys_alias = dim_tempo_keys.alias("tempo")
dim_artista_keys_alias = dim_artista_keys.alias("artista")

# Faz joins com as dimensões para formar o fato
fato_df = df_alias \
    .join(dim_filme_keys_alias, col("df.imdb_id_local") == col("filme.imdb_id"), "left") \
    .join(dim_tempo_keys_alias,
          (col("filme.ano_lancamento") == col("tempo.ano_lancamento")) & (col("filme.mes_lancamento") == col("tempo.mes_lancamento")),
          "left") \
    .join(dim_artista_keys_alias, col("df.nomeartista") == col("artista.nomeartista"), "left")

# Seleciona colunas relevantes para o fato popularidade
fato_popularidade_df = fato_df.select(
    col("filme.filme_id"),
    col("tempo.tempo_id"),
    col("artista.artista_principal_id"),
    col("produtora1_id"),
    col("produtora2_id"),
    col("produtora3_id"),

    col("filme.ano_lancamento"),
    col("filme.mes_lancamento"),

    col("notamedia"),
    col("numerovotos"),
    col("weighted_rating"),
    col("budget"),
    col("revenue"),

    col("cast_count"),
    col("cast_popularity_0_3"),
    col("cast_popularity_3_7"),
    col("cast_popularity_7_10"),

    col("composers_count"),
    col("composers_pop_0_3"),
    col("composers_pop_3_7"),
    col("composers_pop_7_10"),

    col("directors_count"),
    col("directors_pop_0_3"),
    col("directors_pop_3_7"),
    col("directors_pop_7_10"),

    col("writers_count"),
    col("writers_pop_0_3"),
    col("writers_pop_3_7"),
    col("writers_pop_7_10"),
)

# Cria chave surrogate para tabela fato
window_fato = Window.orderBy("filme_id", "tempo_id", "artista_principal_id", "produtora1_id", "produtora2_id", "produtora3_id")
fato_popularidade_df = fato_popularidade_df.withColumn("fato_id", row_number().over(window_fato))

# Salva as dimensões e fato em parquet particionado
dim_tempo_df.write.mode("overwrite").partitionBy("ano_lancamento", "mes_lancamento").parquet(f"{args['S3_TARGET_BASE_PATH']}/DimTempo/")
dim_filme_df.write.mode("overwrite").partitionBy("ano_lancamento", "mes_lancamento").parquet(f"{args['S3_TARGET_BASE_PATH']}/DimFilme/")
dim_artista_df.write.mode("overwrite").parquet(f"{args['S3_TARGET_BASE_PATH']}/DimArtistaPrincipal/")
dim_produtora_df.write.mode("overwrite").parquet(f"{args['S3_TARGET_BASE_PATH']}/DimProdutora/")
fato_popularidade_df.write.mode("overwrite").partitionBy("ano_lancamento", "mes_lancamento").parquet(f"{args['S3_TARGET_BASE_PATH']}/FatoPopularidade/")

# Finaliza o job Glue
job.commit()
