import json
import logging
import time
import os
import requests
import boto3
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes da API
ENDPOINT_FIND = '/find'
ENDPOINT_MOVIE = '/movie'
EXTERNAL_SOURCE_IMDB = 'imdb_id'
APPEND_RESPONSE = 'keywords,external_ids'

# Códigos de status HTTP
HTTP_RATE_LIMIT = 429
HTTP_NOT_FOUND = 404

# Constantes de configuração
DEFAULT_BATCH_SIZE = 100
DEFAULT_RATE_LIMIT_DELAY = 0.25

def _obter_configuracao_ambiente() -> Dict[str, Any]:
    """Obtém e valida as configurações do ambiente"""
    try:
        tmdb_api_key = os.environ.get('TMDB_API_KEY')
        tmdb_base_url = os.environ.get('TMDB_BASE_URL')
        s3_bucket = os.environ.get('S3_BUCKET')
        
        # Configurações com valores padrão
        batch_size = int(os.environ.get('BATCH_SIZE', DEFAULT_BATCH_SIZE))
        rate_limit_delay = float(os.environ.get('RATE_LIMIT_DELAY', DEFAULT_RATE_LIMIT_DELAY))
        
        # Validações obrigatórias
        if not tmdb_api_key:
            raise ValueError("TMDB_API_KEY não configurado")
        if not tmdb_base_url:
            raise ValueError("TMDB_BASE_URL não configurado")
        if not s3_bucket:
            raise ValueError("S3_BUCKET não configurado")
        
        return {
            'tmdb_api_key': tmdb_api_key,
            'tmdb_base_url': tmdb_base_url,
            's3_bucket': s3_bucket,
            'batch_size': batch_size,
            'rate_limit_delay': rate_limit_delay
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Erro na configuração: {str(e)}")
        raise

class ConsultorTMDB:
    """Classe responsável por consultar dados de filmes na API TMDB"""
    
    def __init__(self):
        """Inicializa o consultor TMDB com validação das configurações"""
        config = _obter_configuracao_ambiente()
        
        self.api_key = config['tmdb_api_key']
        self.base_url = config['tmdb_base_url']
        self.s3_bucket = config['s3_bucket']
        self.batch_size = config['batch_size']
        self.rate_limit_delay = config['rate_limit_delay']
        
        self.session = requests.Session()
        self.s3_client = boto3.client('s3') if self.s3_bucket else None
    
    def obter_detalhes_filme_por_id_imdb(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        """Obtém detalhes completos de um filme usando ID IMDB"""
        if not imdb_id or not isinstance(imdb_id, str):
            logger.warning(f"ID IMDB inválido: {imdb_id}")
            return None
            
        try:
            # Converte IMDB ID para TMDB ID
            tmdb_id = self._obter_tmdb_id_por_imdb_id(imdb_id)
            if not tmdb_id:
                return None
            
            # Busca detalhes completos usando TMDB ID
            return self._obter_detalhes_filme_por_tmdb_id(tmdb_id, imdb_id)
            
        except Exception as e:
            logger.error(f"Erro ao processar filme {imdb_id}: {str(e)}")
            return None
    
    def _obter_tmdb_id_por_imdb_id(self, imdb_id: str) -> Optional[int]:
        """Converte IMDB ID para TMDB ID usando endpoint /find"""
        try:
            self._aguardar_rate_limit()
            
            url = f"{self.base_url}{ENDPOINT_FIND}/{imdb_id}"
            params = {
                'api_key': self.api_key,
                'external_source': EXTERNAL_SOURCE_IMDB
            }
            
            response = self._fazer_requisicao_com_retry(url, params)
            if not response:
                return None
            
            dados_busca = response.json()
            resultados_filmes = dados_busca.get('movie_results', [])
            
            if not resultados_filmes:
                logger.warning(f"Filme não encontrado: {imdb_id}")
                return None
            
            # Pega o primeiro resultado (mais relevante)
            tmdb_id = resultados_filmes[0].get('id')
            if not tmdb_id:
                logger.warning(f"TMDB ID não encontrado: {imdb_id}")
                return None
            
            return tmdb_id
            
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Erro ao converter IMDB ID {imdb_id}: {str(e)}")
            return None
    
    def _obter_detalhes_filme_por_tmdb_id(self, tmdb_id: int, imdb_id_original: str) -> Optional[Dict[str, Any]]:
        """Obtém detalhes completos de um filme usando endpoint /movie"""
        try:
            self._aguardar_rate_limit()
            
            url = f"{self.base_url}{ENDPOINT_MOVIE}/{tmdb_id}"
            params = {
                'api_key': self.api_key,
                'append_to_response': APPEND_RESPONSE
            }
            
            response = self._fazer_requisicao_com_retry(url, params)
            if not response:
                return None
            
            dados_filme = response.json()
            return self._formatar_dados_filme(dados_filme, imdb_id_original)
            
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Erro ao obter detalhes do filme {tmdb_id}: {str(e)}")
            return None
    
    def _fazer_requisicao_com_retry(self, url: str, params: Dict[str, Any]) -> Optional[requests.Response]:
        """Faz requisição HTTP com tratamento de rate limit e retry"""
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == HTTP_RATE_LIMIT:
                logger.warning("Rate limit atingido, aguardando...")
                time.sleep(1)
                response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == HTTP_NOT_FOUND:
                logger.warning(f"Recurso não encontrado: {url}")
                return None
            
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            logger.error(f"Erro na requisição HTTP: {str(e)}")
            return None
    
    def _aguardar_rate_limit(self) -> None:
        """Aguarda o tempo necessário para respeitar o rate limit"""
        time.sleep(self.rate_limit_delay)
    
    def _formatar_dados_filme(self, dados_filme: Dict[str, Any], imdb_id_original: str) -> Dict[str, Any]:
        """Formata os dados do filme no formato especificado"""
        try:
            # Extrai e formata gêneros
            generos = dados_filme.get('genres', [])
            generos_str = ', '.join(genero['name'] for genero in generos if isinstance(genero, dict) and 'name' in genero)
            
            # Extrai e formata palavras-chave
            palavras_chave = dados_filme.get('keywords', {}).get('keywords', [])
            palavras_chave_str = ', '.join(kw['name'] for kw in palavras_chave if isinstance(kw, dict) and 'name' in kw)
            
            # Extrai e formata países de produção
            paises_producao = dados_filme.get('production_countries', [])
            paises_str = ', '.join(pais['name'] for pais in paises_producao if isinstance(pais, dict) and 'name' in pais)
            
            # Usa IMDB ID original ou extrai do external_ids
            ids_externos = dados_filme.get('external_ids', {})
            imdb_id = ids_externos.get('imdb_id', imdb_id_original)
            
            return {
                "imdb_id": imdb_id,
                "tmdb_genres": generos_str,
                "tmdb_keywords": palavras_chave_str,
                "tmdb_revenue": dados_filme.get('revenue', 0),
                "tmdb_budget": dados_filme.get('budget', 0),
                "tmdb_release_date": dados_filme.get('release_date', ''),
                "tmdb_production_countries": paises_str,
                "tmdb_popularity": dados_filme.get('popularity', 0.0),
                "tmdb_adult": dados_filme.get('adult', False)
            }
            
        except Exception as e:
            logger.error(f"Erro ao formatar dados: {str(e)}")
            return {}
    
    def salvar_no_s3(self, dados: List[Dict[str, Any]], caminho_s3: str, numero_batch: int) -> None:
        """Salva dados de filmes no S3"""
        if not self.s3_client or not dados:
            return

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"tmdb_filmes_batch_{numero_batch}_{timestamp}.json"
            chave_s3 = f"{caminho_s3}/{nome_arquivo}"
            
            dados_json = json.dumps(dados, ensure_ascii=False, indent=2)
            
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=chave_s3,
                Body=dados_json,
                ContentType='application/json'
            )
            
            logger.info(f"Dados salvos: s3://{self.s3_bucket}/{chave_s3}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar no S3: {str(e)}")

def processar_ids_filmes(consultor: ConsultorTMDB, ids_filmes: List[str]) -> List[Dict[str, Any]]:
    """Processa uma lista de IDs de filmes e retorna os dados formatados"""
    if not ids_filmes:
        return []
        
    resultados = []
    
    for id_filme in ids_filmes:
        dados_filme = consultor.obter_detalhes_filme_por_id_imdb(id_filme)
        if dados_filme:
            resultados.append(dados_filme)
    
    return resultados

def lambda_handler(evento: Dict[str, Any], contexto: Any) -> Dict[str, Any]:
    """
    Handler principal do AWS Lambda
    Processa uma lista de até 100 IDs de filmes (formato IMDB)
    """
    try:
        # Extrai parâmetros do evento
        ids_filmes = evento.get('movie_ids')
        numero_batch = evento.get('batch_number')
        caminho_s3 = evento.get('s3_path')
        
        # Validações
        if not ids_filmes or not isinstance(ids_filmes, list):
            raise ValueError("Lista de movie_ids vazia ou inválida")
        
        # Obtém configuração para validação do batch size
        config = _obter_configuracao_ambiente()
        batch_size = config['batch_size']
        
        if len(ids_filmes) > batch_size:
            raise ValueError(f"Lista excede limite de {batch_size}. Recebidos: {len(ids_filmes)}")
        
        logger.info(f"Iniciando: {len(ids_filmes)} filmes, batch {numero_batch}")
        
        # Processa filmes
        consultor = ConsultorTMDB()
        tempo_inicio = time.time()
        resultados = processar_ids_filmes(consultor, ids_filmes)
        tempo_execucao = time.time() - tempo_inicio
        
        # Prepara resposta
        resposta = {
            "status": "success",
            "data": resultados,
            "metadata": {
                "total_movies_processed": len(resultados),
                "total_movies_requested": len(ids_filmes),
                "batch_number": numero_batch,
                "execution_time": tempo_execucao,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Salva no S3
        consultor.salvar_no_s3(resultados, caminho_s3, numero_batch)
        
        logger.info(f"Concluído: {len(resultados)}/{len(ids_filmes)} filmes em {tempo_execucao:.2f}s")
        return resposta
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
