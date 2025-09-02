#!/usr/bin/env python3
"""
Orquestrador para AWS Lambda - Consultor TMDB
Script responsável por orquestrar as chamadas do Lambda para processar múltiplas páginas
"""

import boto3
import json
import time
import os
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

# Carrega variáveis do arquivo .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
    print(" Arquivo .env carregado com sucesso")
except ImportError:
    print("  python-dotenv não instalado. Instale com: pip install python-dotenv")
except Exception as e:
    print(f" Erro ao carregar .env: {e}")

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constantes de configuração
COLUNAS_ID_POSSIVEIS = ['id', 'movie_id', 'tmdb_id', 'movieId', 'imdb_id']
FORMATO_IMDB_PREFIXO = 'tt'
FORMATO_IMDB_TAMANHO_MIN = 9  # tt + 7 dígitos
FORMATO_IMDB_TAMANHO_MAX = 10  # tt + 8 dígitos
FORMATO_IMDB_DIGITOS_MIN = 7
FORMATO_IMDB_DIGITOS_MAX = 8

# Valores padrão para configurações
DEFAULT_LAMBDA_TIMEOUT = 900
DEFAULT_MAX_RETRY_ATTEMPTS = 3
DEFAULT_BATCH_SIZE = 100
DEFAULT_DELAY_BETWEEN_BATCHES = 1.0

def _obter_configuracao_ambiente() -> Dict[str, Any]:
    """Obtém e valida as configurações do ambiente"""
    try:
        # Configurações obrigatórias
        nome_funcao = os.environ.get('LAMBDA_FUNCTION_NAME')
        regiao_lambda = os.environ.get('LAMBDA_REGION')
        bucket_s3 = os.environ.get('S3_BUCKET')
        caminho_base_saida_s3 = os.environ.get('S3_OUTPUT_BASE_PATH')
        
        # Configurações com valores padrão
        timeout_lambda = int(os.environ.get('LAMBDA_TIMEOUT', DEFAULT_LAMBDA_TIMEOUT))
        max_tentativas_retry = int(os.environ.get('MAX_RETRY_ATTEMPTS', DEFAULT_MAX_RETRY_ATTEMPTS))
        tipo_invocacao_lambda = os.environ.get('LAMBDA_INVOCATION_TYPE', 'RequestResponse')
        tamanho_batch = int(os.environ.get('BATCH_SIZE', DEFAULT_BATCH_SIZE))
        
        # Validações obrigatórias
        if not nome_funcao:
            raise ValueError("LAMBDA_FUNCTION_NAME não configurado")
        if not regiao_lambda:
            raise ValueError("LAMBDA_REGION não configurado")
        if not bucket_s3:
            raise ValueError("S3_BUCKET não configurado")
        if not caminho_base_saida_s3:
            raise ValueError("S3_OUTPUT_BASE_PATH não configurado")
        
        return {
            'nome_funcao': nome_funcao,
            'regiao_lambda': regiao_lambda,
            'timeout_lambda': timeout_lambda,
            'max_tentativas_retry': max_tentativas_retry,
            'tipo_invocacao_lambda': tipo_invocacao_lambda,
            'bucket_s3': bucket_s3,
            'caminho_base_saida_s3': caminho_base_saida_s3,
            'tamanho_batch': tamanho_batch
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Erro na configuração: {str(e)}")
        raise

class OrquestradorLambda:
    """Classe responsável por orquestrar as chamadas do Lambda para processar filmes"""
    
    def __init__(self):
        """Inicializa o orquestrador com validação das configurações"""
        config = _obter_configuracao_ambiente()
        
        self.nome_funcao = config['nome_funcao']
        self.regiao_lambda = config['regiao_lambda']
        self.timeout_lambda = config['timeout_lambda']
        self.max_tentativas_retry = config['max_tentativas_retry']
        self.tipo_invocacao_lambda = config['tipo_invocacao_lambda']
        self.bucket_s3 = config['bucket_s3']
        self.caminho_base_saida_s3 = config['caminho_base_saida_s3']
        self.tamanho_batch = config['tamanho_batch']
        
        self._inicializar_clientes_aws()
        self._configurar_logging()
        
        logger.info(f"Orquestrador inicializado - Função: {self.nome_funcao}, Região: {self.regiao_lambda}")
    
    def _inicializar_clientes_aws(self) -> None:
        """Inicializa os clientes AWS necessários"""
        self.cliente_lambda = boto3.client('lambda', region_name=self.regiao_lambda)
        self.cliente_s3 = boto3.client('s3')
    
    def _configurar_logging(self) -> None:
        """Configura o nível de logging baseado na variável de ambiente"""
        nivel_log = os.environ.get('LOG_LEVEL', 'INFO')
        logging.getLogger().setLevel(getattr(logging, nivel_log.upper()))

    def ler_ids_filmes_do_csv(self, caminho_csv_s3: str) -> List[str]:
        """Lê a lista de IDs de filmes (formato IMDB) de um arquivo CSV no S3"""
        if not caminho_csv_s3 or not isinstance(caminho_csv_s3, str):
            raise ValueError("Caminho do CSV inválido")
            
        try:
            logger.info(f"Lendo CSV: s3://{self.bucket_s3}/{caminho_csv_s3}")
            
            # Baixa e lê o arquivo CSV
            conteudo_csv = self._baixar_csv_do_s3(caminho_csv_s3)
            df = pd.read_csv(pd.io.common.BytesIO(conteudo_csv))
            
            # Identifica e valida a coluna de ID
            coluna_id = self._identificar_coluna_id(df)
            ids_filmes = df[coluna_id].dropna().unique().tolist()
            
            # Valida formato IMDB
            ids_validos = self._validar_ids_imdb(ids_filmes)
            
            logger.info(f"Encontrados {len(ids_validos)} IDs IMDB válidos")
            return ids_validos
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {str(e)}")
            raise
    
    def _baixar_csv_do_s3(self, caminho_csv_s3: str) -> bytes:
        """Baixa o arquivo CSV do S3"""
        try:
            resposta = self.cliente_s3.get_object(Bucket=self.bucket_s3, Key=caminho_csv_s3)
            return resposta['Body'].read()
        except Exception as e:
            logger.error(f"Erro ao baixar CSV: {str(e)}")
            raise
    
    def _identificar_coluna_id(self, df: pd.DataFrame) -> str:
        """Identifica a coluna que contém os IDs de filmes"""
        for coluna in COLUNAS_ID_POSSIVEIS:
            if coluna in df.columns:
                return coluna
        
        raise ValueError(f"Coluna de ID não encontrada. Colunas: {list(df.columns)}")
    
    def _validar_ids_imdb(self, ids_filmes: List[Any]) -> List[str]:
        """Valida se os IDs estão no formato IMDB correto (tt + 7 ou 8 dígitos)"""
        ids_validos = []
        
        for id_filme in ids_filmes:
            id_str = str(id_filme).strip()
            
            if (id_str.startswith(FORMATO_IMDB_PREFIXO) and 
                FORMATO_IMDB_TAMANHO_MIN <= len(id_str) <= FORMATO_IMDB_TAMANHO_MAX and 
                id_str[2:].isdigit()):
                ids_validos.append(id_str)
            else:
                logger.warning(f"ID inválido (tt + 7-8 dígitos): {id_str}")
        
        return ids_validos
    
    def invocar_lambda_batch(self, ids_filmes: List[str], numero_batch: int, caminho_s3: str) -> Dict[str, Any]:
        """Invoca o Lambda para processar um batch de IDs de filmes"""
        if not ids_filmes or not isinstance(ids_filmes, list):
            return {"status": "error", "error": "Lista de IDs inválida"}
            
        try:
            payload = {
                "movie_ids": ids_filmes,
                "batch_number": numero_batch,
                "s3_path": caminho_s3
            }
            
            logger.info(f"Invocando batch {numero_batch}: {len(ids_filmes)} filmes")
            
            # Invoca o Lambda com retry
            for tentativa in range(self.max_tentativas_retry):
                try:
                    resposta = self._fazer_invocacao_lambda(payload)
                    return self._processar_resposta_lambda(resposta, numero_batch)
                    
                except Exception as e:
                    logger.warning(f"Tentativa {tentativa + 1} falhou para batch {numero_batch}: {str(e)}")
                    if tentativa < self.max_tentativas_retry - 1:
                        self._aguardar_backoff_exponencial(tentativa)
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Erro ao invocar Lambda para batch {numero_batch}: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _fazer_invocacao_lambda(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Faz a invocação do Lambda"""
        try:
            return self.cliente_lambda.invoke(
                FunctionName=self.nome_funcao,
                InvocationType=self.tipo_invocacao_lambda,
                Payload=json.dumps(payload)
            )
        except Exception as e:
            logger.error(f"Erro na invocação: {str(e)}")
            raise
    
    def _processar_resposta_lambda(self, resposta: Dict[str, Any], numero_batch: int) -> Dict[str, Any]:
        """Processa a resposta do Lambda"""
        try:
            payload_resposta = json.loads(resposta['Payload'].read())
            
            if resposta['StatusCode'] == 200 and payload_resposta.get('status') == 'success':
                filmes_processados = payload_resposta['metadata']['total_movies_processed']
                logger.info(f"Batch {numero_batch} sucesso: {filmes_processados} filmes")
                return payload_resposta
            else:
                erro = payload_resposta.get('error', 'Erro desconhecido')
                logger.error(f"Erro no batch {numero_batch}: {erro}")
                return payload_resposta
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _aguardar_backoff_exponencial(self, tentativa: int) -> None:
        """Aguarda tempo exponencial entre tentativas"""
        tempo_espera = 2 ** tentativa
        time.sleep(tempo_espera)
    
    def processar_ids_filmes_em_batches(self, todos_ids_filmes: List[str], caminho_s3: str, delay_entre_batches: float = DEFAULT_DELAY_BETWEEN_BATCHES) -> Dict[str, Any]:
        """Processa uma lista completa de IDs de filmes em batches"""
        if not todos_ids_filmes:
            return {"status": "error", "error": "Lista de IDs vazia"}
        
        # Divide em batches
        batches = self._dividir_em_batches(todos_ids_filmes)
        logger.info(f"Iniciando: {len(todos_ids_filmes)} filmes em {len(batches)} batches")
        
        # Processa cada batch
        resultados = self._processar_batches(batches, caminho_s3, delay_entre_batches)
        
        return self._criar_resposta_final(resultados, todos_ids_filmes, len(batches))
    
    def _dividir_em_batches(self, ids_filmes: List[str]) -> List[List[str]]:
        """Divide a lista de IDs em batches do tamanho configurado"""
        return [ids_filmes[i:i + self.tamanho_batch] 
                for i in range(0, len(ids_filmes), self.tamanho_batch)]
    
    def _processar_batches(self, batches: List[List[str]], caminho_s3: str, delay_entre_batches: float) -> Dict[str, Any]:
        """Processa todos os batches sequencialmente"""
        todos_resultados = []
        total_processados = 0
        tempo_inicio = time.time()
        
        for numero_batch, ids_filmes_batch in enumerate(batches, 1):
            logger.info(f"Processando batch {numero_batch}/{len(batches)} ({len(ids_filmes_batch)} filmes)")
            
            resultado = self.invocar_lambda_batch(ids_filmes_batch, numero_batch, caminho_s3)
            
            if resultado.get('status') == 'success':
                dados_batch = resultado.get('data', [])
                todos_resultados.extend(dados_batch)
                total_processados += resultado['metadata']['total_movies_processed']
                logger.info(f"Batch {numero_batch} concluído: {len(dados_batch)} filmes")
            else:
                logger.error(f"Falha no batch {numero_batch}: {resultado.get('error')}")
            
            # Aguarda entre batches (exceto no último)
            if numero_batch < len(batches) and delay_entre_batches > 0:
                logger.info(f"Aguardando {delay_entre_batches}s...")
                time.sleep(delay_entre_batches)
        
        return {
            'resultados': todos_resultados,
            'total_processados': total_processados,
            'tempo_inicio': tempo_inicio
        }
    
    def _criar_resposta_final(self, resultados: Dict[str, Any], todos_ids_filmes: List[str], total_batches: int) -> Dict[str, Any]:
        """Cria a resposta final com metadados"""
        tempo_execucao = time.time() - resultados['tempo_inicio']
        
        return {
            "status": "success",
            "total_movies_processed": resultados['total_processados'],
            "total_movies_requested": len(todos_ids_filmes),
            "total_batches_processed": total_batches,
            "data": resultados['resultados'],
            "metadata": {
                "start_time": datetime.fromtimestamp(resultados['tempo_inicio']).isoformat(),
                "end_time": datetime.now().isoformat(),
                "execution_time": tempo_execucao,
                "execution_summary": f"Processados {resultados['total_processados']} filmes em {total_batches} batches"
            }
        }

def _obter_configuracoes_adicionais() -> Dict[str, Any]:
    """Obtém configurações adicionais do ambiente"""
    try:
        delay_entre_batches = float(os.environ.get('DELAY_BETWEEN_BATCHES', DEFAULT_DELAY_BETWEEN_BATCHES))
        caminho_csv_s3 = os.environ.get('CSV_S3_PATH')
        
        if not caminho_csv_s3:
            raise ValueError("CSV_S3_PATH não configurado")
        
        # Limpa o caminho se incluir s3:// e bucket
        bucket_s3 = os.environ.get('S3_BUCKET')
        if caminho_csv_s3.startswith('s3://'):
            caminho_csv_s3 = caminho_csv_s3.replace('s3://', '').replace(f"{bucket_s3}/", '')
        
        return {
            'delay_entre_batches': delay_entre_batches,
            'caminho_csv_s3': caminho_csv_s3
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Erro nas configurações: {str(e)}")
        raise

def _construir_caminho_s3() -> str:
    """Constrói o caminho S3 com data atual"""
    hoje = datetime.now()
    caminho_base_saida_s3 = os.environ.get('S3_OUTPUT_BASE_PATH')
    if not caminho_base_saida_s3:
        raise ValueError("S3_OUTPUT_BASE_PATH não configurado")
    
    return f"{caminho_base_saida_s3}/{hoje.strftime('%Y')}/{hoje.strftime('%m')}/{hoje.strftime('%d')}"

def _exibir_resultados(resultado: Dict[str, Any], caminho_s3: str) -> None:
    """Exibe os resultados do processamento"""
    if resultado['status'] == 'success':
        logger.info("Processamento concluído!")
        logger.info(f"Resumo:")
        logger.info(f"  - Filmes processados: {resultado['total_movies_processed']}")
        logger.info(f"  - Filmes solicitados: {resultado['total_movies_requested']}")
        logger.info(f"  - Batches processados: {resultado['total_batches_processed']}")
        logger.info(f"  - Tempo total: {resultado['metadata']['execution_time']:.2f}s")
        logger.info(f"  - Caminho S3: {caminho_s3}")
        
        _salvar_resultado_local(resultado)
    else:
        logger.error(f"Erro no processamento: {resultado.get('error')}")

def _salvar_resultado_local(resultado: Dict[str, Any]) -> None:
    """Salva o resultado em arquivo local se configurado"""
    try:
        salvar_resultado_local = os.environ.get('SAVE_LOCAL_RESULT', 'true').lower() == 'true'
        if salvar_resultado_local:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo_local = os.environ.get('LOCAL_RESULT_FILENAME', 'orquestrador_result')
            nome_arquivo = f"{nome_arquivo_local}_{timestamp}.json"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Resultado salvo: {nome_arquivo}")
    except Exception as e:
        logger.error(f"Erro ao salvar resultado: {str(e)}")

def main() -> None:
    """Função principal do orquestrador"""
    try:
        # Obtém configurações
        config_adicional = _obter_configuracoes_adicionais()
        caminho_s3 = _construir_caminho_s3()
        
        logger.info("Iniciando orquestrador")
        logger.info(f"CSV de entrada: {config_adicional['caminho_csv_s3']}")
        logger.info(f"Caminho S3 de saída: {caminho_s3}")
        
        # Executa processamento
        orquestrador = OrquestradorLambda()
        todos_ids_filmes = orquestrador.ler_ids_filmes_do_csv(config_adicional['caminho_csv_s3'])
        
        resultado = orquestrador.processar_ids_filmes_em_batches(
            todos_ids_filmes, caminho_s3, config_adicional['delay_entre_batches']
        )
        
        # Exibe e salva resultados
        _exibir_resultados(resultado, caminho_s3)
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")

if __name__ == "__main__":
    main()
