import boto3
import json
import os
import time
from dotenv import load_dotenv
from botocore.config import Config

# Carrega variáveis do .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")  # opcional
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_BUCKET = "data-lake-rhamon-pires-pb"
S3_PREFIX = "Raw/Local/CSV/Movies Filtrados ID/2025/07/21/"

LAMBDA_FUNCTION_NAME = "sprint05-etapa2-carregar-json"
CONNECTION_TIMEOUT=60
READ_TIMEOUT=600

# Clientes Boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION
)

# Configuração de timeout para Lambda
config = Config(
    region_name=AWS_REGION,
    connect_timeout=CONNECTION_TIMEOUT,
    read_timeout=READ_TIMEOUT
)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    config=config
)

def listar_arquivos_csv(bucket, prefix):
    """Retorna uma lista dos arquivos CSV dentro do prefixo no S3."""
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    arquivos = []

    for obj in response.get('Contents', []):

        key = obj['Key']

        if key.endswith('.csv'):
            arquivos.append(key)

    return arquivos

def invocar_lambdas():

    arquivos_csv = listar_arquivos_csv(S3_BUCKET, S3_PREFIX)

    if not arquivos_csv:
        print(f"Nenhum arquivo CSV encontrado no prefixo {S3_PREFIX}")
        return

    for i, csv_key in enumerate(arquivos_csv, 1):
        
        payload = {
            "csv_s3_key": csv_key
        }

        print(f"\nInvocando Lambda para CSV {i}/{len(arquivos_csv)}: {csv_key}")

        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',  # espera resposta síncrona
            Payload=json.dumps(payload)
        )

        response_payload = json.loads(response['Payload'].read())
        print("Resposta do Lambda:")
        print(json.dumps(response_payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    invocar_lambdas()
