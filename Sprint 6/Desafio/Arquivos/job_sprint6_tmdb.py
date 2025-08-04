import sys
from urllib.parse import urlparse
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import lit

# Recebe os parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

# Inicializa contextos
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# Extrai ano, mes e dia do caminho S3
parsed_path = urlparse(input_path)
path_parts = parsed_path.path.strip("/").split("/")
year = int(path_parts[-3])
month = int(path_parts[-2])
day = int(path_parts[-1])

# Leitura JSON com Spark
df = spark.read.option("multiline", "true").json(input_path)

# Converte para pandas para manipulação
df_pd = df.toPandas()

# Remove colunas
cols_to_drop = [
    "tmdb_id",
    "titulo_original",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "generos",
]
df_pd.drop(columns=cols_to_drop, inplace=True)

# Renomeia a coluna 'titulo' para 'tituloBR'
df_pd.rename(columns={"titulo": "tituloBR"}, inplace=True)

# Volta para Spark DataFrame
df = spark.createDataFrame(df_pd)

# Adiciona colunas de partição ano, mês e dia
df = df.withColumn("year", lit(year)) \
       .withColumn("month", lit(month)) \
       .withColumn("day", lit(day))

# Escreve em parquet particionado
df.write.mode("overwrite").partitionBy("year", "month", "day").parquet(target_path)

job.commit()
