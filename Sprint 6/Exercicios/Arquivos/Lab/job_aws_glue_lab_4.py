import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import pyspark.sql.functions as pysfunc

# @params: [JOB_NAME, S3_INPUT_PATH, S3_TARGET_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# 1. Leitura do CSV
dyn_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [source_file]},
    format="csv",
    format_options={"withHeader": True, "separator": ","}
)

# 2. Imprimir o schema
dyn_df.printSchema()

# Converter para DataFrame
df = dyn_df.toDF()

# Converter 'total' para inteiro
df = df.withColumn("total", pysfunc.col("total").cast("int"))

# 3. Nome em MAIÚSCULO
df_upper = df.withColumn("nome", pysfunc.upper(pysfunc.col("nome")))

# 4. Contagem total de linhas
print("Contagem total de linhas:", df_upper.count())

# 5. Contagem de nomes por ano e sexo, ordenado pelo ano decrescente
grouped = (
    df_upper.groupBy("ano", "sexo")
        .agg(pysfunc.sum("total").alias("total"))
        .orderBy(pysfunc.col("ano").desc())
)
grouped.show()

# 6. Nome feminino mais frequente
fem_top = (
    df_upper.filter(pysfunc.col("sexo") == "F")
        .groupBy("ano", "nome")
        .agg(pysfunc.sum("total").alias("total"))
        .orderBy(pysfunc.desc("total"))
        .limit(1)
)
fem_top.show()

# Nome masculino mais frequente
masc_top = (
    df_upper.filter(pysfunc.col("sexo") == "M")
        .groupBy("ano", "nome")
        .agg(pysfunc.sum("total").alias("total"))
        .orderBy(pysfunc.desc("total"))
        .limit(1)
)
masc_top.show()

# Total de registros por ano, primeiros 10 anos ordenados crescente
total_ano = (
    df_upper.groupBy("ano")
        .agg(pysfunc.sum("total").alias("total"))
        .orderBy(pysfunc.col("ano").asc())
        .limit(10)
)
total_ano.show()

# Gravação no S3 em JSON, particionado por sexo e ano
df_dyn_final = DynamicFrame.fromDF(df_upper, glueContext, "df_dyn_final")

glueContext.write_dynamic_frame.from_options(
    frame=df_dyn_final,
    connection_type="s3",
    connection_options={
        "path": target_path,
        "partitionKeys": ["sexo", "ano"]
    },
    format="json"
)

job.commit()
