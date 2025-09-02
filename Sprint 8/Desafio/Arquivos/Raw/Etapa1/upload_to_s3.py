"""
Script simples para upload de arquivos CSV para Amazon S3
Organiza os arquivos em estrutura hierárquica por tipo e data
"""

import os
import boto3
from datetime import datetime
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constantes
ARQUIVOS_CSV = ['movies.csv', 'series.csv', 'filmes_romance_drama_filtrados.csv']
MAPEAMENTO_DIRETORIOS = {
    'movies': 'Movies',
    'series': 'Series',
    'filmes_romance_drama_filtrados': 'Movies (Drama Romance)'
}

def carregar_configuracao():
    """Carrega as configurações do arquivo .env"""
    load_dotenv('.env')
    
    config = {
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'aws_session_token': os.getenv('AWS_SESSION_TOKEN'),
        'aws_default_region': os.getenv('AWS_DEFAULT_REGION'),
        'local_data_dir': os.getenv('LOCAL_DATA_DIR'),
        's3_base_path': os.getenv('S3_BASE_PATH')
    }
    
    return config

def criar_cliente_s3(config):
    """Cria e retorna o cliente S3"""
    try:
        # Parâmetros básicos
        params = {
            'service_name': 's3',
            'aws_access_key_id': config['aws_access_key_id'],
            'aws_secret_access_key': config['aws_secret_access_key'],
            'region_name': config['aws_default_region']
        }
        
        # Adicionar token de sessão se existir
        if config.get('aws_session_token'):
            params['aws_session_token'] = config['aws_session_token']
        
        s3_client = boto3.client(**params)
        return s3_client
    except Exception as e:
        logger.error(f"Erro ao criar cliente S3: {e}")
        raise

def obter_caminho_data():
    """Retorna o caminho da data atual no formato ano/mes/dia"""
    hoje = datetime.now()
    return f"{hoje.year}/{hoje.month:02d}/{hoje.day:02d}"

def obter_nome_diretorio(nome_arquivo):
    """Cria o nome do diretório baseado no nome do arquivo CSV"""
    nome_sem_extensao = nome_arquivo.replace('.csv', '')
    return MAPEAMENTO_DIRETORIOS.get(nome_sem_extensao, nome_sem_extensao)

def extrair_bucket_chave(caminho_s3):
    """Extrai bucket e chave de um caminho S3"""
    if not caminho_s3.startswith('s3://'):
        raise ValueError(f"Caminho S3 inválido: {caminho_s3}")
    
    caminho_sem_protocolo = caminho_s3[5:]
    partes = caminho_sem_protocolo.split('/', 1)
    bucket = partes[0]
    chave = partes[1] if len(partes) > 1 else ""
    
    return bucket, chave

def fazer_upload_arquivo(s3_client, caminho_local, bucket, chave):
    """Faz upload de um arquivo para o S3"""
    try:
        logger.info(f"Fazendo upload de {caminho_local} para s3://{bucket}/{chave}")
        s3_client.upload_file(caminho_local, bucket, chave)
        logger.info(f"Upload concluído com sucesso: s3://{bucket}/{chave}")
        return True
    except Exception as e:
        logger.error(f"Erro no upload de {caminho_local}: {e}")
        return False

def main():
    """Função principal para fazer upload dos CSVs"""
    try:
        # Carregar configurações
        config = carregar_configuracao()
        logger.info("Configurações carregadas com sucesso")
        
        # Criar cliente S3
        s3_client = criar_cliente_s3(config)
        logger.info("Cliente S3 criado com sucesso")
        
        # Obter caminho da data atual
        caminho_data = obter_caminho_data()
        logger.info(f"Usando caminho de data: {caminho_data}")
        
        # Fazer upload de cada arquivo
        sucessos = 0
        falhas = 0
        
        for arquivo in ARQUIVOS_CSV:
            caminho_local = os.path.join(config['local_data_dir'], arquivo)
            
            # Verificar se o arquivo existe
            if not os.path.exists(caminho_local):
                logger.warning(f"Arquivo não encontrado: {caminho_local}")
                falhas += 1
                continue
            
            # Criar nome do diretório baseado no nome do arquivo
            nome_diretorio = obter_nome_diretorio(arquivo)
            
            # Construir caminho S3 completo com diretório e data
            caminho_s3_completo = f"{config['s3_base_path']}/{nome_diretorio}/{caminho_data}/{arquivo}"
            
            # Extrair bucket e chave do caminho S3
            bucket, chave = extrair_bucket_chave(caminho_s3_completo)
            
            # Fazer upload
            if fazer_upload_arquivo(s3_client, caminho_local, bucket, chave):
                sucessos += 1
                logger.info(f"✓ Upload de {arquivo} concluído com sucesso")
            else:
                falhas += 1
                logger.error(f"✗ Falha no upload de {arquivo}")
        
        # Resumo final
        logger.info(f"Processo finalizado - Sucessos: {sucessos}, Falhas: {falhas}")
        
    except Exception as e:
        logger.error(f"Erro durante o processo de upload: {e}")
        raise

if __name__ == "__main__":
    main()
