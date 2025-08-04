import sys
import pandas as pd
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Receber argumentos
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# Define esquema
schema = StructType([
    StructField("id", StringType(), True),
    StructField("tituloPrincipal", StringType(), True),
    StructField("tituloOriginal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("tempoMinutos", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notaMedia", DoubleType(), True),
    StructField("numeroVotos", IntegerType(), True),
    StructField("generoArtista", StringType(), True),
    StructField("personagem", StringType(), True),
    StructField("nomeArtista", StringType(), True),
    StructField("anoNascimento", IntegerType(), True),
    StructField("anoFalecimento", IntegerType(), True),
    StructField("profissao", StringType(), True),
    StructField("titulosMaisConhecidos", StringType(), True)
])

# Lê CSV no Spark
df_spark = spark.read.csv(source_file, header=False, schema=schema, sep="|")

# Converte para pandas
df = df_spark.toPandas()

# Filtro de gêneros (case insensitive)
df = df[df['genero'].str.lower().isin(['drama', 'romance'])]

# Remove linhas com notaMedia ou numeroVotos nulos
df = df[df['notaMedia'].notnull() & df['numeroVotos'].notnull()]

# Calcula C e m
C = df['notaMedia'].mean()
m = df['numeroVotos'].quantile(0.95)

def weighted_rating(x, m=m, C=C):
    v = x['numeroVotos']
    R = x['notaMedia']
    return (v / (v + m) * R) + (m / (v + m) * C)

df['weighted_rating'] = df.apply(weighted_rating, axis=1)

# Filtra filmes que passam no critério
df = df[(df['numeroVotos'] >= m) & (df['weighted_rating'] > 7)]

# Remove colunas indesejadas
cols_to_drop = ['tituloOriginal', 'anoLancamento', 'personagem', 'anoNascimento', 'anoFalecimento', 'profissao']
df = df.drop(columns=cols_to_drop)

# Volta para Spark DataFrame
df_final_spark = spark.createDataFrame(df)

# Escreve Parquet
df_final_spark.write.mode("overwrite").parquet(target_path)

job.commit()